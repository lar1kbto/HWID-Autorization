"""
Модуль для получения уникального аппаратного идентификатора (HWID)
"""
import hashlib
import platform
import uuid
import subprocess
import re


def get_machine_guid():
    """Получить Machine GUID из реестра Windows (самый стабильный метод)"""
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(
                'reg query "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Cryptography" /v MachineGuid',
                shell=True,
                stderr=subprocess.DEVNULL,
                encoding='cp866'  # Кодировка для русской Windows
            )
            
            # Извлекаем GUID из вывода
            match = re.search(r'MachineGuid\s+REG_SZ\s+([A-F0-9\-]+)', result, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    except Exception:
        return None


def get_system_uuid():
    """Получить UUID системы через getnode()"""
    try:
        # Получаем MAC-адрес (самый стабильный идентификатор)
        mac = uuid.getnode()
        if mac:
            return str(mac)
        return None
    except Exception:
        return None


def get_cpu_serial():
    """Получить серийный номер процессора через wmic"""
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(
                "wmic cpu get ProcessorId",
                shell=True,
                stderr=subprocess.DEVNULL,
                encoding='cp866',
                timeout=5
            )
            
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            # Пропускаем заголовок "ProcessorId"
            if len(lines) >= 2:
                cpu_id = lines[1].strip()
                if cpu_id and cpu_id != "ProcessorId":
                    return cpu_id
        
        return None
    except Exception:
        return None


def get_motherboard_serial():
    """Получить серийный номер материнской платы"""
    try:
        if platform.system() == "Windows":
            result = subprocess.check_output(
                "wmic baseboard get SerialNumber",
                shell=True,
                stderr=subprocess.DEVNULL,
                encoding='cp866',
                timeout=5
            )
            
            lines = [line.strip() for line in result.split('\n') if line.strip()]
            if len(lines) >= 2:
                serial = lines[1].strip()
                if serial and serial != "SerialNumber":
                    return serial
        
        return None
    except Exception:
        return None


def get_hwid():
    """
    Получить уникальный HWID системы
    Использует комбинацию нескольких идентификаторов для максимальной стабильности
    """
    identifiers = []
    
    # 1. Machine GUID (самый стабильный)
    machine_guid = get_machine_guid()
    if machine_guid:
        identifiers.append(f"GUID:{machine_guid}")
    
    # 2. MAC-адрес
    system_uuid = get_system_uuid()
    if system_uuid:
        identifiers.append(f"MAC:{system_uuid}")
    
    # 3. CPU ID (если доступен)
    cpu_serial = get_cpu_serial()
    if cpu_serial:
        identifiers.append(f"CPU:{cpu_serial}")
    
    # 4. Серийный номер материнской платы
    mb_serial = get_motherboard_serial()
    if mb_serial:
        identifiers.append(f"MB:{mb_serial}")
    
    # Если есть хотя бы один идентификатор
    if identifiers:
        # Объединяем все идентификаторы и хешируем
        combined = "|".join(identifiers)
        hwid_hash = hashlib.sha256(combined.encode()).hexdigest()
        return hwid_hash.upper()
    
    # Если совсем ничего не получилось (очень маловероятно)
    return "ERROR: Не удалось получить HWID"


if __name__ == "__main__":
    # Тест модуля
    hwid = get_hwid()
    print(f"HWID: {hwid}")
