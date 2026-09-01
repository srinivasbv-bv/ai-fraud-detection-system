import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class FrameworkMappingEngine:
    """
    Maps transaction fraud types to standard Fraud Lifecycle Stages,
    OWASP API Security Top 10 (2023), and PCI DSS v4.0 Control References.
    """
    def __init__(self):
        self.mappings = config.FRAUD_FRAMEWORK_MAPPINGS

    def map_transaction(self, fraud_type):
        mapping = self.mappings.get(fraud_type, self.mappings["LEGITIMATE"])
        return {
            "category_code": fraud_type,
            "category_name": mapping["name"],
            "lifecycle_stage": mapping["lifecycle_stage"],
            "owasp_reference": mapping["owasp_ref"],
            "pci_dss_reference": mapping["pci_dss_ref"],
            "description": mapping["description"]
        }

    def get_all_mappings(self):
        return self.mappings
