#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSCA Seed Export Script v2.0
导出当前OSCA配置为可移植的种子文件

用法:
    python export_seed.py <seed-name> [output-dir]
    
示例:
    python export_seed.py webdev-frontend
    python export_seed.py gamedev-unity ./seeds/exported
    
v2.0 更新:
    - 支持种子库模式 (seeds/library/)
    - 支持 Cell 文件导出
    - 支持细粒度 Skills 导出
"""

import os
import sys
import shutil
import yaml
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List


def get_osca_root() -> Path:
    """获取OSCA根目录（脚本所在目录的父目录）"""
    return Path(__file__).parent.parent.resolve()


def load_osca_config(osca_root: Path) -> Dict:
    """加载OSCA-CONFIG.yaml"""
    config_path = osca_root / "OSCA-CONFIG.yaml"
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def generate_timestamp() -> str:
    """生成时间戳"""
    return datetime.now().strftime("%Y-%m-%d_%H%M%S")


def calculate_checksum(file_path: Path) -> str:
    """计算文件SHA256校验和"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()[:16]


def scan_seed_library(osca_root: Path) -> List[str]:
    """扫描种子库中的种子"""
    library_dir = osca_root / "seeds" / "library"
    if not library_dir.exists():
        return []
    
    seeds = []
    for seed_file in library_dir.glob("*.seed.yaml"):
        seeds.append(seed_file.stem.replace('.seed', ''))
    return sorted(seeds)


def scan_cells(osca_root: Path) -> List[str]:
    """扫描Cell文件"""
    cells_dir = osca_root / "cells"
    if not cells_dir.exists():
        return []
    
    cells = []
    for cell_file in cells_dir.glob("*.cell"):
        cells.append(cell_file.stem)
    return sorted(cells)


def scan_skills(osca_root: Path) -> Dict[str, List[str]]:
    """扫描细粒度Skills"""
    skills_dir = osca_root / "skills"
    if not skills_dir.exists():
        return {}
    
    skills = {
        'stem_cell': [],
        'fine_grained': []
    }
    
    # 元技能
    stem_cell_dir = skills_dir / "_stem-cell"
    if stem_cell_dir.exists():
        skills['stem_cell'].append("_stem-cell/SKILL.md")
    
    # 细粒度 Skills
    for skill_file in skills_dir.rglob("*.skill"):
        rel_path = skill_file.relative_to(skills_dir)
        skills['fine_grained'].append(str(rel_path))
    
    return skills


def export_seed_from_library(seed_name: str, output_dir: Path, osca_root: Path) -> Path:
    """从种子库导出种子（v2.0 推荐方式）"""
    library_dir = osca_root / "seeds" / "library"
    seed_file = library_dir / f"{seed_name}.seed.yaml"
    
    if not seed_file.exists():
        raise FileNotFoundError(f"种子 {seed_name} 不存在于种子库中")
    
    timestamp = generate_timestamp()
    export_file = output_dir / f"{seed_name}-{timestamp}.seed.yaml"
    
    # 读取种子内容
    with open(seed_file, 'r', encoding='utf-8') as f:
        seed_content = yaml.safe_load(f)
    
    # 添加导出元信息
    seed_content['seed']['meta']['exported_at'] = datetime.now().isoformat()
    seed_content['seed']['meta']['exported_by'] = "export_seed.py v2.0"
    seed_content['seed']['meta']['export_checksum'] = calculate_checksum(seed_file)
    
    # 导出关联的 Cell 文件
    cell_file_name = seed_content.get('seed', {}).get('cell', {}).get('cell_file', '')
    if cell_file_name:
        cell_file = osca_root / cell_file_name
        if cell_file.exists():
            cell_export = output_dir / f"{seed_name}-{timestamp}.cell"
            shutil.copy2(cell_file, cell_export)
    
    # 保存种子文件
    output_dir.mkdir(parents=True, exist_ok=True)
    with open(export_file, 'w', encoding='utf-8') as f:
        yaml.dump(seed_content, f, allow_unicode=True, sort_keys=False)
    
    return export_file


def create_full_seed_package_v2(seed_name: str, output_dir: Path, osca_root: Path) -> Path:
    """创建完整的种子包（v2.0 - 包含 Seed/Cell/Skills）"""
    timestamp = generate_timestamp()
    package_name = f"{seed_name}-{timestamp}"
    package_dir = output_dir / package_name
    
    # 创建目录结构
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "seeds" / "library").mkdir(parents=True, exist_ok=True)
    (package_dir / "cells").mkdir(exist_ok=True)
    (package_dir / "skills").mkdir(exist_ok=True)
    
    # 复制种子文件
    library_dir = osca_root / "seeds" / "library"
    seed_file = library_dir / f"{seed_name}.seed.yaml"
    if seed_file.exists():
        shutil.copy2(seed_file, package_dir / "seeds" / "library" / f"{seed_name}.seed.yaml")
    
    # 读取种子获取 Cell 引用
    if seed_file.exists():
        with open(seed_file, 'r', encoding='utf-8') as f:
            seed_content = yaml.safe_load(f)
        cell_file_name = seed_content.get('seed', {}).get('cell', {}).get('cell_file', '')
        if cell_file_name:
            cell_file = osca_root / cell_file_name
            if cell_file.exists():
                shutil.copy2(cell_file, package_dir / "cells" / cell_file.name)
    
    # 复制相关的 Skills
    skills = scan_skills(osca_root)
    src_skills = osca_root / "skills"
    dst_skills = package_dir / "skills"
    
    for skill_path in skills.get('stem_cell', []):
        src = src_skills / skill_path
        if src.exists():
            dst = dst_skills / skill_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    
    # 创建 manifest
    manifest = {
        "name": seed_name,
        "version": "2.0.0",
        "exported_at": datetime.now().isoformat(),
        "osca_version": "2.0.0",
        "architecture": "Seed/Cell/Skills",
        "contents": [
            "seeds/library/*.seed.yaml",
            "cells/*.cell",
            "skills/**/*.skill",
            "skills/_stem-cell/SKILL.md"
        ],
        "install_command": f"python import_seed.py {package_name}.zip [--register]"
    }
    
    with open(package_dir / "seed-manifest.json", 'w', encoding='utf-8') as f:
        yaml.dump(manifest, f, allow_unicode=True)
    
    # 创建 zip 包
    zip_file = shutil.make_archive(
        base_name=str(output_dir / package_name),
        format='zip',
        root_dir=str(package_dir.parent),
        base_dir=package_name
    )
    
    # 清理临时目录
    shutil.rmtree(package_dir)
    
    return Path(zip_file)


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("=" * 60)
        print("OSCA Seed Export Tool v2.0")
        print("=" * 60)
        print()
        print("用法: python export_seed.py <seed-name> [output-dir]")
        print()
        print("从种子库导出种子:")
        print("  python export_seed.py webdev")
        print("  python export_seed.py gamedev-unity ./seeds/exported")
        print()
        print("v2.0 特性:")
        print("  - 支持种子库模式 (seeds/library/)")
        print("  - 自动包含关联的 Cell 文件")
        print("  - 包含细粒度 Skills")
        print()
        sys.exit(1)
    
    seed_name = sys.argv[1]
    osca_root = get_osca_root()
    config = load_osca_config(osca_root)
    
    # 确定输出目录
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2]).resolve()
    else:
        output_dir = osca_root / "seeds" / "exported"
    
    print("=" * 60)
    print("OSCA Seed Export Tool v2.0")
    print("=" * 60)
    print()
    print(f"种子名称: {seed_name}")
    print(f"OSCA根目录: {osca_root}")
    print(f"OSCA版本: {config.get('meta', {}).get('version', 'unknown')}")
    print(f"输出目录: {output_dir}")
    print()
    
    # 显示种子库信息
    library_seeds = scan_seed_library(osca_root)
    print(f"种子库中可用种子: {', '.join(library_seeds) if library_seeds else '无'}")
    print()
    
    try:
        # 创建完整种子包
        print("正在创建 v2.0 种子包...")
        print("包含: Seed + Cell + Skills")
        seed_package = create_full_seed_package_v2(seed_name, output_dir, osca_root)
        
        print()
        print("=" * 60)
        print("✅ 种子导出成功!")
        print("=" * 60)
        print()
        print(f"完整包: {seed_package}")
        print(f"大小: {seed_package.stat().st_size:,} bytes")
        print()
        print("v2.0 包内容:")
        print("  - seeds/library/{seed}.seed.yaml  (领域定义)")
        print("  - cells/{seed}.cell               (Skill清单/行动模式)")
        print("  - skills/**/*.skill               (细粒度执行单元)")
        print()
        print("使用方法:")
        print(f"  python import_seed.py \"{seed_package.name}\" --register")
        print()
        
    except FileNotFoundError as e:
        print()
        print("❌ 错误: 种子不存在!")
        print(f"原因: {e}")
        print()
        print("可用种子:")
        for seed in library_seeds:
            print(f"  - {seed}")
        sys.exit(1)
        
    except Exception as e:
        print()
        print("❌ 错误: 导出失败!")
        print(f"原因: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
