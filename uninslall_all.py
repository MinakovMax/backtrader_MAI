import os
import subprocess

# Получаем список установленных пакетов
packages = subprocess.check_output(['pip', 'freeze']).decode('utf-8').split('\n')

# Фильтруем и обрабатываем каждый пакет
for package in packages:
    if package:
        package_name = package.split('==')[0]
        # Удаляем пакет, игнорируя ошибки
        subprocess.call(['pip', 'uninstall', '-y', package_name])

print("Все установленные пакеты были удалены.")