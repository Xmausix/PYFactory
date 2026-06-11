from constants import MODULE_TYPES


class ModuleSystem:
    @staticmethod
    def install(building, module_type: str) -> bool:
        if module_type not in MODULE_TYPES:
            return False
        if not hasattr(building, "module"):
            return False
        building.module = module_type
        return True

    @staticmethod
    def remove(building) -> str | None:
        if hasattr(building, "module") and building.module:
            mod = building.module
            building.module = None
            return mod
        return None

    @staticmethod
    def get_info(module_type: str) -> dict:
        return MODULE_TYPES.get(module_type, {})