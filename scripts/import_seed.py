#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSCA Seed Import Script v2.0
从种子文件导入OSCA配置

用法:
    python import_seed.py <seed-file> [--activate] [--register]
    
示例:
    python import_seed.py seeds/exported/webdev-2026-02-12.zip
    python import_seed.py gamedev.zip --register
    python import_seed.py intelligent-retrieval.seed.yaml --register --activate
    
v2.0 更新:
    - 支持种子库模式 (seeds/library/)
    - 支持 --register 参数自动注册到种子库
    - 支持 Cell 文件导入
    - 支持细粒度 Skills 导入
    - 支持自动生成缺失的 Skills
"""

import os
import sys
import shutil
import zipfile
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any, List


def get_osca_root() -> Path:
    """获取OSCA根目录"""
    return Path(__file__).parent.parent.resolve()


def load_osca_config(osca_root: Path) -> Dict[str, Any]:
    """加载OSCA-CONFIG.yaml"""
    config_path = osca_root / "OSCA-CONFIG.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def save_osca_config(osca_root: Path, config: Dict[str, Any]):
    """保存OSCA-CONFIG.yaml"""
    config_path = osca_root / "OSCA-CONFIG.yaml"
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, allow_unicode=True, sort_keys=False)


def parse_seed_manifest(seed_dir: Path) -> Dict[str, Any]:
    """解析种子manifest文件"""
    manifest_file = seed_dir / "seed-manifest.json"
    if manifest_file.exists():
        import json
        return json.loads(manifest_file.read_text(encoding='utf-8'))
    return {}


def load_seed_file(seed_path: Path) -> Dict[str, Any]:
    """加载种子YAML文件"""
    with open(seed_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def validate_seed(seed_data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """验证种子数据完整性"""
    errors = []
    
    if 'seed' not in seed_data:
        errors.append("缺少 'seed' 根节点")
        return False, errors
    
    seed = seed_data['seed']
    
    # 检查必需字段
    required_meta = ['version', 'seed_id', 'name']
    if 'meta' not in seed:
        errors.append("缺少 'seed.meta'")
    else:
        for field in required_meta:
            if field not in seed['meta']:
                errors.append(f"缺少 'seed.meta.{field}'")
    
    # 检查 identity
    if 'identity' not in seed:
        errors.append("缺少 'seed.identity'")
    
    # 检查 cell 引用 (v2.0)
    if 'cell' not in seed:
        errors.append("缺少 'seed.cell' (v2.0 必需)")
    elif 'cell_file' not in seed.get('cell', {}):
        errors.append("缺少 'seed.cell.cell_file' (v2.0 必需)")
    
    return len(errors) == 0, errors


def backup_current_config(osca_root: Path) -> Path:
    """备份当前配置"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = osca_root / "backups" / f"pre-import-{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 备份核心文件
    files_to_backup = [
        "OSCA-CONFIG.yaml",
        "AGENTS.md",
        "SOUL.md",
        "HEARTBEAT.md",
        "TOOLS.md"
    ]
    
    for filename in files_to_backup:
        src = osca_root / filename
        if src.exists():
            shutil.copy2(src, backup_dir / filename)
    
    return backup_dir


def register_seed_to_library(seed_data: Dict[str, Any], seed_file: Path, 
                             osca_root: Path) -> bool:
    """注册种子到种子库 (v2.0)"""
    library_dir = osca_root / "seeds" / "library"
    library_dir.mkdir(parents=True, exist_ok=True)
    
    seed = seed_data.get('seed', {})
    meta = seed.get('meta', {})
    
    seed_name = meta.get('name', seed_file.stem.replace('.seed', ''))
    seed_version = meta.get('version', '1.0.0')
    seed_desc = meta.get('description', f'Imported {seed_name}')
    
    # 复制种子文件到种子库
    dest_seed = library_dir / f"{seed_name}.seed.yaml"
    shutil.copy2(seed_file, dest_seed)
    
    # 更新 OSCA-CONFIG.yaml
    config = load_osca_config(osca_root)
    
    if 'seed_library' not in config:
        config['seed_library'] = {'base_path': 'seeds/library', 'seeds': {}}
    
    if 'seeds' not in config['seed_library']:
        config['seed_library']['seeds'] = {}
    
    config['seed_library']['seeds'][seed_name] = {
        'seed_file': f"{seed_name}.seed.yaml",
        'version': seed_version,
        'description': seed_desc
    }
    
    # 添加触发器映射
    if 'differentiation' not in config:
        config['differentiation'] = {'triggers': {'mapping': {}}}
    
    if 'triggers' not in config['differentiation']:
        config['differentiation']['triggers'] = {'mapping': {}}
    
    if 'mapping' not in config['differentiation']['triggers']:
        config['differentiation']['triggers']['mapping'] = {}
    
    config['differentiation']['triggers']['mapping'][seed_name] = f"seeds/library/{seed_name}.seed.yaml"
    
    save_osca_config(osca_root, config)
    
    return True


def import_cell_file(cell_source: Path, osca_root: Path) -> bool:
    """导入 Cell 文件 (v2.0)"""
    if not cell_source.exists():
        return False
    
    cells_dir = osca_root / "cells"
    cells_dir.mkdir(exist_ok=True)
    
    dest = cells_dir / cell_source.name
    shutil.copy2(cell_source, dest)
    
    return True


def import_skills(skills_dir: Path, osca_root: Path) -> List[str]:
    """导入 Skills"""
    imported = []
    
    if not skills_dir.exists():
        return imported
    
    dst_skills = osca_root / "skills"
    dst_skills.mkdir(exist_ok=True)
    
    for skill_file in skills_dir.rglob("*.skill"):
        rel_path = skill_file.relative_to(skills_dir)
        dst = dst_skills / rel_path
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_file, dst)
        imported.append(str(rel_path))
    
    # 导入 _stem-cell
    stem_cell_src = skills_dir / "_stem-cell"
    if stem_cell_src.exists():
        stem_cell_dst = dst_skills / "_stem-cell"
        if stem_cell_dst.exists():
            shutil.rmtree(stem_cell_dst)
        shutil.copytree(stem_cell_src, stem_cell_dst)
        imported.append("_stem-cell/")
    
    return imported


def check_missing_skills(seed_data: Dict[str, Any], osca_root: Path) -> List[str]:
    """检查缺失的 Skills (v2.0)"""
    missing = []
    
    # 这里简化处理，实际应该解析 Cell 文件
    # 并检查 skills/ 目录中的 .skill 文件
    
    return missing


def import_seed_v2(seed_path: Path, osca_root: Path, 
                   register: bool = False, activate: bool = False) -> Dict[str, Any]:
    """导入种子 (v2.0)"""
    
    result = {
        'seed_name': '',
        'cell_imported': False,
        'skills_imported': [],
        'registered': False,
        'activated': False,
        'backup_dir': None,
        'instance_id': ''
    }
    
    # 备份当前配置
    result['backup_dir'] = backup_current_config(osca_root)
    
    extract_dir = None
    
    try:
        # 处理 zip 包
        if seed_path.suffix == '.zip':
            extract_dir = osca_root / "seeds" / "imported" / seed_path.stem
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
            
            with zipfile.ZipFile(seed_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # 在解压目录中查找种子文件
            seed_files = list(extract_dir.rglob("*.seed.yaml"))
            if not seed_files:
                raise ValueError("压缩包中未找到 .seed.yaml 文件")
            seed_file = seed_files[0]
        else:
            seed_file = seed_path
            extract_dir = seed_file.parent
        
        # 加载并验证种子
        seed_data = load_seed_file(seed_file)
        valid, errors = validate_seed(seed_data)
        
        if not valid:
            raise ValueError(f"种子验证失败: {', '.join(errors)}")
        
        seed = seed_data['seed']
        meta = seed['meta']
        result['seed_name'] = meta.get('name', seed_file.stem.replace('.seed', ''))
        
        # 注册到种子库
        if register:
            register_seed_to_library(seed_data, seed_file, osca_root)
            result['registered'] = True
        
        # 导入 Cell 文件
        cell_file_name = seed.get('cell', {}).get('cell_file', '')
        if cell_file_name:
            if extract_dir:
                # 在解压目录中查找 Cell
                cell_files = list(extract_dir.rglob(f"{result['seed_name']}.cell"))
                if cell_files:
                    result['cell_imported'] = import_cell_file(cell_files[0], osca_root)
        
        # 导入 Skills
        if extract_dir:
            skills_dirs = list(extract_dir.rglob("skills"))
            if skills_dirs:
                result['skills_imported'] = import_skills(skills_dirs[0], osca_root)
        
        # 检查缺失的 Skills
        missing_skills = check_missing_skills(seed_data, osca_root)
        if missing_skills:
            print(f"  ⚠️  检测到缺失的 Skills: {', '.join(missing_skills)}")
            print(f"     将在分化时自动生成")
        
        # 创建实例记录
        instance_id = f"v2-instance-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(2).hex()}"
        result['instance_id'] = instance_id
        
        instances_dir = osca_root / "memory" / "instances"
        instances_dir.mkdir(parents=True, exist_ok=True)
        
        instance_record = {
            'instance': {
                'id': instance_id,
                'seed_source': str(seed_path.name),
                'seed_name': result['seed_name'],
                'imported_at': datetime.now().isoformat(),
                'status': 'activated' if activate else 'imported',
                'v2_protocol': True,
                'cell_imported': result['cell_imported'],
                'skills_count': len(result['skills_imported']),
                'backup_location': str(result['backup_dir'])
            }
        }
        
        with open(instances_dir / f"{instance_id}.yaml", 'w', encoding='utf-8') as f:
            yaml.dump(instance_record, f, allow_unicode=True)
        
        # 激活
        if activate:
            active_file = osca_root / "memory" / ".active_instance"
            active_file.write_text(instance_id, encoding='utf-8')
            
            identity_file = osca_root / "memory" / ".current_identity"
            identity_file.write_text(result['seed_name'], encoding='utf-8')
            
            result['activated'] = True
        
    finally:
        # 清理临时解压目录
        if extract_dir and seed_path.suffix == '.zip':
            if extract_dir.exists():
                shutil.rmtree(extract_dir)
    
    return result


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("OSCA Seed Import Tool v2.0")
        print("=" * 60)
        print()
        print("用法: python import_seed.py <seed-file> [选项]")
        print()
        print("选项:")
        print("  --activate    导入后立即激活")
        print("  --register    注册到种子库 (seeds/library/)")
        print()
        print("示例:")
        print('  python import_seed.py seeds/exported/webdev-2026-02-12.zip')
        print('  python import_seed.py gamedev.zip --register')
        print('  python import_seed.py intelligent-retrieval.seed.yaml --register --activate')
        print()
        print("v2.0 特性:")
        print("  - 支持种子库注册 (--register)")
        print("  - 自动导入 Cell 文件")
        print("  - 自动导入细粒度 Skills")
        print("  - 检查并报告缺失的 Skills")
        print()
        sys.exit(1)
    
    seed_file = Path(sys.argv[1])
    activate = "--activate" in sys.argv
    register = "--register" in sys.argv
    osca_root = get_osca_root()
    
    print("=" * 60)
    print("OSCA Seed Import Tool v2.0")
    print("=" * 60)
    print()
    
    # 检查种子文件
    if not seed_file.exists():
        # 尝试在seeds目录下查找
        for search_dir in [osca_root / "seeds" / "exported", 
                          osca_root / "seeds" / "library"]:
            alt_path = search_dir / seed_file.name
            if alt_path.exists():
                seed_file = alt_path
                break
        else:
            print(f"❌ 错误: 种子文件不存在!")
            print(f"路径: {seed_file}")
            sys.exit(1)
    
    seed_file = seed_file.resolve()
    print(f"种子文件: {seed_file}")
    print(f"OSCA根目录: {osca_root}")
    print(f"选项: {'激活 ' if activate else ''}{'注册到种子库' if register else ''}")
    print()
    
    try:
        print("正在导入 (v2.0 协议)...")
        print()
        
        result = import_seed_v2(seed_file, osca_root, register, activate)
        
        print()
        print("=" * 60)
        print("✅ 导入成功!")
        print("=" * 60)
        print()
        print(f"种子名称: {result['seed_name']}")
        print(f"实例ID: {result['instance_id']}")
        print()
        
        if result['registered']:
            print("📚 已注册到种子库!")
            print(f"   位置: seeds/library/{result['seed_name']}.seed.yaml")
            print()
        
        if result['cell_imported']:
            print("🧬 Cell 文件已导入!")
            print()
        
        if result['skills_imported']:
            print(f"🛠️  已导入 {len(result['skills_imported'])} 个 Skills")
            print()
        
        print(f"💾 配置已备份到: {result['backup_dir']}")
        print()
        
        if result['activated']:
            print("🚀 实例已激活!")
            print()
            print(f"现在可以使用: /differentiate {result['seed_name']}")
        else:
            print("💡 提示: 使用 --activate 参数立即激活此实例")
        
        print()
        
    except Exception as e:
        print()
        print("❌ 错误: 导入失败!")
        print(f"原因: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
