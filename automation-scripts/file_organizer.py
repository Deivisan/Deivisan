#!/usr/bin/env python3
"""
🤖 File Organizer - DeiviTech Automation Script
===============================================

Script para organização automática de arquivos por extensão.
Parte da coleção DeiviTech Automation Scripts.

Autor: Deivison Santana
Email: deivilsantana@outlook.com
Versão: 2.0 (FASE 2)
Data: Janeiro 2025
"""

import argparse
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("file_organizer.log"), logging.StreamHandler()],
)


class FileOrganizer:
    """Organizador de arquivos por extensão"""

    def __init__(self, base_folder: str):
        self.base_folder = Path(base_folder)
        self.stats = {"moved_files": 0, "created_folders": 0, "errors": 0}

        # Mapeamento de extensões para pastas
        self.extension_map = {
            "imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"],
            "documentos": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
            "planilhas": [".xls", ".xlsx", ".csv", ".ods"],
            "apresentacoes": [".ppt", ".pptx", ".odp"],
            "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
            "audios": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
            "arquivos": [".zip", ".rar", ".7z", ".tar", ".gz"],
            "programas": [".exe", ".msi", ".deb", ".rpm", ".dmg"],
            "scripts": [".py", ".js", ".html", ".css", ".php", ".sql"],
        }

    def create_folders(self) -> None:
        """Cria as pastas de organização"""
        for folder_name in self.extension_map.keys():
            folder_path = self.base_folder / folder_name
            if not folder_path.exists():
                folder_path.mkdir(exist_ok=True)
                self.stats["created_folders"] += 1
                logging.info(f"📁 Pasta criada: {folder_name}")

    def get_file_category(self, file_extension: str) -> str:
        """Determina a categoria do arquivo baseada na extensão"""
        for category, extensions in self.extension_map.items():
            if file_extension.lower() in extensions:
                return category
        return "outros"

    def move_file(self, file_path: Path, destination_folder: str) -> bool:
        """Move arquivo para pasta de destino"""
        try:
            dest_path = self.base_folder / destination_folder
            if not dest_path.exists():
                dest_path.mkdir(exist_ok=True)
                self.stats["created_folders"] += 1

            # Verifica se arquivo já existe no destino
            dest_file = dest_path / file_path.name
            if dest_file.exists():
                # Adiciona timestamp para evitar sobrescrita
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                name, ext = file_path.stem, file_path.suffix
                dest_file = dest_path / f"{name}_{timestamp}{ext}"

            shutil.move(str(file_path), str(dest_file))
            self.stats["moved_files"] += 1
            logging.info(f"📄 Movido: {file_path.name} → {destination_folder}/")
            return True

        except Exception as e:
            self.stats["errors"] += 1
            logging.error(f"❌ Erro ao mover {file_path.name}: {e}")
            return False

    def organize(self, create_backup: bool = False) -> Dict:
        """Organiza todos os arquivos da pasta"""
        if not self.base_folder.exists():
            raise FileNotFoundError(f"Pasta não encontrada: {self.base_folder}")

        # Backup opcional
        if create_backup:
            self.create_backup()

        # Cria pastas de organização
        self.create_folders()

        # Processa todos os arquivos
        for file_path in self.base_folder.iterdir():
            if file_path.is_file():
                file_extension = file_path.suffix
                category = self.get_file_category(file_extension)
                self.move_file(file_path, category)

        # Log final
        logging.info("✅ Organização concluída!")
        logging.info("📊 Estatísticas:")
        logging.info(f"   - Arquivos movidos: {self.stats['moved_files']}")
        logging.info(f"   - Pastas criadas: {self.stats['created_folders']}")
        logging.info(f"   - Erros: {self.stats['errors']}")

        return self.stats

    def create_backup(self) -> None:
        """Cria backup da estrutura atual"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = (
            self.base_folder.parent / f"backup_{self.base_folder.name}_{timestamp}"
        )

        try:
            shutil.copytree(self.base_folder, backup_folder)
            logging.info(f"💾 Backup criado: {backup_folder}")
        except Exception as e:
            logging.error(f"❌ Erro ao criar backup: {e}")


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description="🤖 DeiviTech File Organizer - Organiza arquivos por extensão"
    )
    parser.add_argument("pasta", help="Caminho da pasta para organizar")
    parser.add_argument(
        "--backup", action="store_true", help="Criar backup antes de organizar"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Simular organização sem mover arquivos"
    )

    args = parser.parse_args()

    try:
        organizer = FileOrganizer(args.pasta)

        if args.dry_run:
            logging.info("🔍 Modo simulação ativado - nenhum arquivo será movido")
            # Implementar lógica de simulação aqui
        else:
            stats = organizer.organize(create_backup=args.backup)

            print("\n" + "=" * 50)
            print("🎯 RELATÓRIO DE ORGANIZAÇÃO")
            print("=" * 50)
            print(f"📄 Arquivos processados: {stats['moved_files']}")
            print(f"📁 Pastas criadas: {stats['created_folders']}")
            print(f"❌ Erros encontrados: {stats['errors']}")
            print("=" * 50)

    except Exception as e:
        logging.error(f"💥 Erro crítico: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
