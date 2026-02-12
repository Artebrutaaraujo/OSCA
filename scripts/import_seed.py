#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSCA Seed Import Script
从种子文件导入OSCA配置

用法:
    python import_seed.py <seed-file> [--activate]
    
示例:
    python import_seed.py seeds/exported/webdev-2026-02-12.zip
    python import_seed.py gamedev.zip --activate
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any


def get_osca_root() -> Path:
    """获取OSCA根目录"""
    return Path(__file__).parent.parent.resolve()


def parse_seed_manifest(seed_dir: Path) -> Dict[str, Any]:
    """解析种子manifest文件"""
    manifest_file = seed_dir / "seed-manifest.json"
    if manifest_file.exists():
        import json
        return json.loads(manifest_file.read_text(encoding='utf-8'))
    return {}


def extract_seed_info(seed_dir: Path) -> Dict[str, str]:
    """提取种子基本信息"""
    info = {
        "name": "unknown",
        "source_identity": "OSCA-STEM"
    }
    
    # 尝试从YAML种子文件解析
    yaml_file = seed_dir / "seed.yaml"
    if yaml_file.exists():
        content = yaml_file.read_text(encoding='utf-8')
        for line in content.split('\n'):
            if 'seed_name:' in line:
                info["name"] = line.split(':')[1].strip().strip('"')
            if 'source:' in line:
                info["source_identity"] = line.split(':')[1].strip().strip('"')
    
    return info


def check_core_files(osca_root: Path) -> tuple:
    """检查核心文件是否存在，返回(缺失数量, 检查结果列表)"""
    core_files = {
        "AGENTS.md": osca_root / "AGENTS.md",
        "SOUL.md": osca_root / "SOUL.md",
        "IDENTITY.md": osca_root / "IDENTITY.md",
        "OSCA-CONFIG.yaml": osca_root / "OSCA-CONFIG.yaml"
    }
    
    results = []
    missing = 0
    
    for name, path in core_files.items():
        if path.exists():
            results.append(f"  ✅ {name} 存在")
        else:
            results.append(f"  ⚠️  {name} 不存在")
            missing += 1
    
    return missing, results


def backup_current_config(osca_root: Path) -> Path:
    """备份当前配置"""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = osca_root / "backups" / f"pre-import-{timestamp}"
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # 备份核心文件
    files_to_backup = [
        "OSCA-CONFIG.yaml",
        "IDENTITY.md",
        "MEMORY.md"
    ]
    
    for filename in files_to_backup:
        src = osca_root / filename
        if src.exists():
            shutil.copy2(src, backup_dir / filename)
    
    return backup_dir


def import_seed_simple(seed_file: Path, osca_root: Path) -> bool:
    """简单导入（仅复制文件，不解压）"""
    import_dir = osca_root / "seeds" / "imported"
    import_dir.mkdir(parents=True, exist_ok=True)
    
    dest = import_dir / seed_file.name
    shutil.copy2(seed_file, dest)
    return True


def import_seed_full(seed_package: Path, osca_root: Path, activate: bool = False) -> str:
    """完整导入（解压并合并）"""
    
    # 创建导入目录
    import_dir = osca_root / "seeds" / "imported"
    import_dir.mkdir(parents=True, exist_ok=True)
    
    # 解压种子包
    extract_dir = import_dir / seed_package.stem
    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    
    with zipfile.ZipFile(seed_package, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    
    # 解析manifest
    manifest = parse_seed_manifest(extract_dir)
    seed_name = manifest.get("name", seed_package.stem)
    
    # 检查核心文件
    missing, check_results = check_core_files(osca_root)
    
    # 备份当前配置
    backup_dir = backup_current_config(osca_root)
    
    # 复制新文件（不覆盖已有文件，除非指定--force）
    files_to_import = [
        "AGENTS.md",
        "SOUL.md",
        "IDENTITY.md",
        "OSCA-CONFIG.yaml",
        "HEARTBEAT.md",
        "TOOLS.md"
    ]
    
    imported = []
    skipped = []
    
    for filename in files_to_import:
        src = extract_dir / filename
        dst = osca_root / filename
        
        if src.exists():
            if dst.exists():
                # 备份旧文件
                shutil.copy2(dst, backup_dir / f"{filename}.old")
                # 覆盖
                shutil.copy2(src, dst)
                imported.append(f"{filename} (覆盖)")
            else:
                shutil.copy2(src, dst)
                imported.append(filename)
    
    # 导入Skills
    src_skills = extract_dir / "skills"
    dst_skills = osca_root / "skills"
    
    if src_skills.exists():
        for skill_dir in src_skills.iterdir():
            if skill_dir.is_dir():
                dst_skill = dst_skills / skill_dir.name
                if dst_skill.exists():
                    # 备份并覆盖
                    backup_skill = backup_dir / "skills" / skill_dir.name
                    backup_skill.mkdir(parents=True, exist_ok=True)
                    shutil.copytree(dst_skill, backup_skill, dirs_exist_ok=True)
                    shutil.rmtree(dst_skill)
                shutil.copytree(skill_dir, dst_skill)
                imported.append(f"skills/{skill_dir.name}")
    
    # 导入记忆
    src_memory = extract_dir / "memory"
    dst_memory = osca_root / "memory"
    
    if src_memory.exists():
        dst_memory.mkdir(exist_ok=True)
        for mem_file in src_memory.glob("*.md"):
            dst_file = dst_memory / mem_file.name
            if not dst_file.exists():
                shutil.copy2(mem_file, dst_file)
                imported.append(f"memory/{mem_file.name}")
    
    # 创建实例记录
    instance_id = f"instance-{datetime.now().strftime('%Y%m%d%H%M%S')}-{os.urandom(2).hex()}"
    instances_dir = osca_root / "memory" / "instances"
    instances_dir.mkdir(parents=True, exist_ok=True)
    
    instance_record = f"""instance:
  id: "{instance_id}"
  seed_source: "{seed_package.name}"
  imported_at: "{datetime.now().isoformat()}"
  status: "{'activated' if activate else 'imported'}"
  seed_name: "{seed_name}"
  backup_location: "{backup_dir}"
"""
    
    (instances_dir / f"{instance_id}.yaml").write_text(instance_record, encoding='utf-8')
    
    # 激活（如果指定）
    if activate:
        active_file = osca_root / "memory" / ".active_instance"
        active_file.write_text(instance_id, encoding='utf-8')
        
        identity_file = osca_root / "memory" / ".current_identity"
        identity_file.write_text(seed_name, encoding='utf-8')
    
    return instance_id


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 50)
        print("OSCA Seed Import Tool")
        print("=" * 50)
        print()
        print("用法: python import_seed.py <seed-file> [--activate]")
        print("示例:")
        print('  python import_seed.py seeds/exported/webdev-2026-02-12.zip')
        print('  python import_seed.py gamedev.zip --activate')
        print()
        sys.exit(1)
    
    seed_file = Path(sys.argv[1])
    activate = "--activate" in sys.argv
    osca_root = get_osca_root()
    
    print("=" * 50)
    print("OSCA Seed Import Tool")
    print("=" * 50)
    print()
    
    # 检查种子文件
    if not seed_file.exists():
        # 尝试在seeds目录下查找
        alt_path = osca_root / "seeds" / "exported" / seed_file.name
        if alt_path.exists():
            seed_file = alt_path
        else:
            print(f"❌ 错误: 种子文件不存在!")
            print(f"路径: {seed_file}")
            sys.exit(1)
    
    seed_file = seed_file.resolve()
    print(f"种子文件: {seed_file}")
    print(f"OSCA根目录: {osca_root}")
    print()
    
    try:
        print("正在导入...")
        
        if seed_file.suffix == '.zip':
            instance_id = import_seed_full(seed_file, osca_root, activate)
        else:
            import_seed_simple(seed_file, osca_root)
            instance_id = f"simple-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        print()
        print("=" * 50)
        print("✅ 导入成功!")
        print("=" * 50)
        print()
        print(f"实例ID: {instance_id}")
        
        if activate:
            print()
            print("🚀 实例已激活!")
            print("你现在可以使用分化的能力了")
        else:
            print()
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
