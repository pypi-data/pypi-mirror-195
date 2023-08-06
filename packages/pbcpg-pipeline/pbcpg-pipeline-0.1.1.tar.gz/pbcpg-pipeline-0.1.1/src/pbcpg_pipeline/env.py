import os
import os.path

MODEL_DIR = os.environ.get('PBCPG_MODEL_DIR',
    os.path.join(os.path.dirname(__file__), 'pileup_calling_model'))
