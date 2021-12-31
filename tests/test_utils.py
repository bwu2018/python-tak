import sys
import os
# script_dir = os.path.dirname(__file__)
# print(script_dir)
# src_dir = os.path.join(script_dir, '..', 'src')
sys.path.append('src')
import utils
import board
import stack
import piece

def test_ij_to_ptn():
    assert 'h8' == utils.ij_to_ptn(0, 7, 8)

def test_ptn_to_ij():
    assert (0,7) == utils.ptn_to_ij('h8', 8)

def test_findCombinations():
    assert ['111', '12', '21'] == utils.findCombinations(3)