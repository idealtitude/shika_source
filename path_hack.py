# A quick workaround for path issues
import os
import bge

os.chdir(bge.logic.expandPath('//'))
