#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OSCA Seed Export Script
导出当前OSCA配置为可移植的种子文件

用法:
    python export_seed.py <seed-name> [output-dir]
    
示例:
    python export_seed.py webdev-frontend
    python export_seed.py gamedev-unity ./seeds
"""

import os
import sys
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional


def get_osca_root() -> Path:
    """获取OSCA根目录（脚本所在目录的父目录）"""
    return Path(__file__).parent.parent.resolve()


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


def scan_skills(osca_root: Path) -> list:
    """扫描已安装的Skill"""
    skills_dir = osca_root / "skills"
    if not skills_dir.exists():
        return []
    
    skills = []
    for skill_dir in skills_dir.iterdir():
        if skill_dir.is_dir() and skill_dir.name != "_stem-cell":
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skills.append(skill_dir.name)
    return sorted(skills)


def create_seed_file(seed_name: str, output_dir: Path, osca_root: Path) -> Path:
    """创建种子文件"""
    timestamp = generate_timestamp()
    seed_file = output_dir / f"{seed_name}-{timestamp}.yaml"
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 扫描技能
    skills = scan_skills(osca_root)
    
    # 检测当前身份
    identity_file = osca_root / "memory" / ".current_identity"
    if identity_file.exists():
        current_identity = identity_file.read_text().strip()
    else:
        current_identity = "OSCA-STEM"
    
    # 检查核心文件
    config_exists = (osca_root / "OSCA-CONFIG.yaml").exists()
    tools_exists = (osca_root / "TOOLS.md").exists()
    heartbeat_exists = (osca_root / "HEARTBEAT.md").exists()
    
    # 生成种子内容
    seed_content = f"""# OSCA Seed File
# Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Export Tool: export_seed.py

seed:
  meta:
    version: "1.0"
    created_by: "OSCA-Ω"
    timestamp: "{datetime.now().isoformat()}"
    export_tool: "export_seed.py"
    seed_name: "{seed_name}"

  identity:
    source: "{current_identity}"

  nucleus:
    # 干细胞核文件 (引用)
    agents_md: "AGENTS.md"
    soul_md: "SOUL.md"
    identity_md: "IDENTITY.md"

  config_summary:
    osca_config: {"\"OSCA-CONFIG.yaml\"" if config_exists else "null"}

  skills:
    stem_cell: "skills/_stem-cell/SKILL.md"
    installed:
{chr(10).join(f'      - "{skill}"' for skill in skills) if skills else '      # 无其他Skill'}

  tools:
    tools_md: {"\"TOOLS.md\"" if tools_exists else "null"}

  heartbeat:
    heartbeat_md: {"\"HEARTBEAT.md\"" if heartbeat_exists else "null"}

# Installation Instructions:
# 1. Copy this seed file to your target OSCA instance
# 2. Run: python import_seed.py {seed_file.name}
# 3. Activate with: --activate flag
"""
    
    # 写入文件
    seed_file.write_text(seed_content, encoding='utf-8')
    
    return seed_file


def copy_core_files(seed_dir: Path, osca_root: Path) -> None:
    """复制核心文件到种子目录"""
    core_files = [
        "AGENTS.md",
        "SOUL.md", 
        "IDENTITY.md",
        "OSCA-CONFIG.yaml",
        "HEARTBEAT.md",
        "TOOLS.md"
    ]
    
    for filename in core_files:
        src = osca_root / filename
        if src.exists():
            shutil.copy2(src, seed_dir / filename)


def copy_skills(seed_dir: Path, osca_root: Path) -> None:
    """复制Skills到种子目录"""
    src_skills = osca_root / "skills"
    dst_skills = seed_dir / "skills"
    
    if src_skills.exists():
        shutil.copytree(src_skills, dst_skills, dirs_exist_ok=True)


def create_full_seed_package(seed_name: str, output_dir: Path, osca_root: Path) -> Path:
    """创建完整的种子包（包含所有文件）"""
    timestamp = generate_timestamp()
    package_name = f"{seed_name}-{timestamp}"
    package_dir = output_dir / package_name
    
    # 创建目录结构
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "skills").mkdir(exist_ok=True)
    (package_dir / "memory").mkdir(exist_ok=True)
    
    # 复制核心文件
    copy_core_files(package_dir, osca_root)
    
    # 复制Skills
    copy_skills(package_dir, osca_root)
    
    # 复制近期记忆（最近30天）
    memory_src = osca_root / "memory"
    memory_dst = package_dir / "memory"
    if memory_src.exists():
        cutoff = datetime.now().timestamp() - (30 * 24 * 60 * 60)
        for mem_file in memory_src.glob("*.md"):
            if mem_file.stat().st_mtime > cutoff:
                shutil.copy2(mem_file, memory_dst)
    
    # 创建manifest
    manifest = f"""{{
  "name": "{seed_name}",
  "version": "1.0.0",
  "exported_at": "{datetime.now().isoformat()}",
  "osca_version": "1.0.0",
  "contents": [
    "AGENTS.md",
    "SOUL.md",
    "IDENTITY.md",
    "OSCA-CONFIG.yaml",
    "HEARTBEAT.md",
    "TOOLS.md",
    "skills/",
    "memory/"
  ],
  "install_command": "python import_seed.py {package_name}.zip [--activate]"
}}"""
    
    (package_dir / "seed-manifest.json").write_text(manifest, encoding='utf-8')
    
    # 创建zip包
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
        print("=" * 50)
        print("OSCA Seed Export Tool")
        print("=" * 50)
        print()
        print("用法: python export_seed.py <seed-name> [output-dir]")
        print("示例:")
        print("  python export_seed.py webdev-frontend")
        print("  python export_seed.py gamedev-unity ./seeds")
        print()
        sys.exit(1)
    
    seed_name = sys.argv[1]
    osca_root = get_osca_root()
    
    # 确定输出目录
    if len(sys.argv) >= 3:
        output_dir = Path(sys.argv[2]).resolve()
    else:
        output_dir = osca_root / "seeds" / "exported"
    
    print("=" * 50)
    print("OSCA Seed Export Tool")
    print("=" * 50)
    print()
    print(f"种子名称: {seed_name}")
    print(f"OSCA根目录: {osca_root}")
    print(f"输出目录: {output_dir}")
    print()
    
    try:
        # 创建完整种子包
        print("正在创建种子包...")
        seed_package = create_full_seed_package(seed_name, output_dir, osca_root)
        
        # 同时创建YAML引用文件
        seed_yaml = create_seed_file(seed_name, output_dir, osca_root)
        
        print()
        print("=" * 50)
        print("✅ 种子导出成功!")
        print("=" * 50)
        print()
        print(f"完整包: {seed_package}")
        print(f"引用文件: {seed_yaml}")
        print(f"大小: {seed_package.stat().st_size} bytes")
        print()
        print("使用方法:")
        print(f"  python import_seed.py \"{seed_package.name}\"")
        print()
        
    except Exception as e:
        print()
        print("❌ 错误: 导出失败!")
        print(f"原因: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
