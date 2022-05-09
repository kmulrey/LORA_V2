# this does basic core / direction fitting with out needing the whole event class structure

import numpy as np
import LORAparameters as LORA
import detector as det
from ROOT import TH1F
from ROOT import TF1
from ROOT import TH2F
from ROOT import TF2
from ROOT import TMath
from ROOT import TVirtualFitter
import math
