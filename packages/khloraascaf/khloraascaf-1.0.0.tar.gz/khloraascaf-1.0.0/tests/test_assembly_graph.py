# -*- coding=utf-8 -*-

"""Unit testing for assembly graph."""

# pylint: disable=compare-to-zero, missing-raises-doc
from pathlib import Path
from typing import Iterator

from revsymg.graphs import RevSymGraph
from revsymg.index_lib import FORWARD_INT, REVERSE_INT, IndexT, IndOrT

from khloraascaf.assembly_graph import AssemblyGraph, OrCT, rev_oriented_contig
from khloraascaf.inputs import STR_ORIENT


# ============================================================================ #
#                                   CONSTANTS                                  #
# ============================================================================ #
TEST_DIR: Path = Path(__file__).parent.absolute()

_TOY_DATADIR = TEST_DIR / 'data'

# ---------------------------------------------------------------------------- #
#                                    IR - UN                                   #
# ---------------------------------------------------------------------------- #
_IR_UN_DIR = _TOY_DATADIR / 'ir_un'
_IR_UN_SOL_REGMAP = _IR_UN_DIR / 'map_of_regions_sol.tsv'
_IR_UN_SOL_REGCTG_F = _IR_UN_DIR / 'contigs_of_regions_sol_0.tsv'
_IR_UN_REG_PATHS = _IR_UN_DIR / 'region_paths.tsv'
_IR_UN_ORC_PATHS = _IR_UN_DIR / 'oriented_contig_paths.tsv'

# ---------------------------------------------------------------------------- #
#                                    DR - UN                                   #
# ---------------------------------------------------------------------------- #
_DR_UN_DIR = _TOY_DATADIR / 'dr_un'
_DR_UN_SOL_REGMAP = _DR_UN_DIR / 'map_of_regions_sol.tsv'
_DR_UN_SOL_REGCTG = _DR_UN_DIR / 'contigs_of_regions_sol.tsv'
_DR_UN_REG_PATHS = _DR_UN_DIR / 'region_paths.tsv'
_DR_UN_ORC_PATHS = _DR_UN_DIR / 'oriented_contig_paths.tsv'


# ============================================================================ #
#                                TEST FUNCTIONS                                #
# ============================================================================ #
# ---------------------------------------------------------------------------- #
#                               All_region_paths                               #
# ---------------------------------------------------------------------------- #
def test_all_region_paths_ir_un():
    """Test all_region_paths method for IR-UN."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _IR_UN_SOL_REGMAP,
        _IR_UN_SOL_REGCTG_F,
    )
    s_region_paths: set[tuple[IndOrT, ...]] = {
        tuple(region_path)
        for region_path in read_region_paths(_IR_UN_REG_PATHS)
    }
    asm_graph_paths = [tuple(l) for l in asm_graph.all_region_paths()]
    assert len(asm_graph_paths) == len(s_region_paths)
    for reg_path in asm_graph_paths:
        assert reg_path in s_region_paths


def test_all_region_paths_dr_un():
    """Test all_region_paths method for DR-UN."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _DR_UN_SOL_REGMAP,
        _DR_UN_SOL_REGCTG,
    )
    s_region_paths: set[tuple[IndOrT, ...]] = {
        tuple(region_path)
        for region_path in read_region_paths(_DR_UN_REG_PATHS)
    }
    asm_graph_paths = [tuple(l) for l in asm_graph.all_region_paths()]
    assert len(asm_graph_paths) == len(s_region_paths)
    for reg_path in asm_graph_paths:
        assert reg_path in s_region_paths


# ---------------------------------------------------------------------------- #
#                           All_oriented_contig_paths                          #
# ---------------------------------------------------------------------------- #
def test_all_oriented_contig_paths_ir_un():
    """Test all_oriented_contig_paths method for IR-UN."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _IR_UN_SOL_REGMAP,
        _IR_UN_SOL_REGCTG_F,
    )
    s_orc_paths: set[tuple[OrCT, ...]] = {
        tuple(orc_path)
        for orc_path in read_oriented_contig_paths(_IR_UN_ORC_PATHS)
    }
    asm_graph_paths = [tuple(l) for l in asm_graph.all_oriented_contig_paths()]
    assert len(asm_graph_paths) == len(s_orc_paths)
    for reg_path in asm_graph_paths:
        assert reg_path in s_orc_paths


def test_all_oriented_contig_paths_dr():
    """Test all_oriented_contig_paths method for DR-UN."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _DR_UN_SOL_REGMAP,
        _DR_UN_SOL_REGCTG,
    )
    s_orc_paths: set[tuple[OrCT, ...]] = {
        tuple(orc_path)
        for orc_path in read_oriented_contig_paths(_DR_UN_ORC_PATHS)
    }
    asm_graph_paths = [tuple(l) for l in asm_graph.all_oriented_contig_paths()]
    assert len(asm_graph_paths) == len(s_orc_paths)
    for reg_path in asm_graph_paths:
        assert reg_path in s_orc_paths


# ---------------------------------------------------------------------------- #
#                                    Revsymg                                   #
# ---------------------------------------------------------------------------- #
def test_getter_revsymg():
    """Test getter revsymg."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _IR_UN_SOL_REGMAP,
        _IR_UN_SOL_REGCTG_F,
    )
    # TOTEST use fixtures and composition
    # TOTEST find a better assertion
    assert isinstance(asm_graph.revsymg(), RevSymGraph)


# ---------------------------------------------------------------------------- #
#                          Oriented_contigs_of_region                          #
# ---------------------------------------------------------------------------- #
def test_oriented_contigs_of_region():
    """Test oriented_contigs_of_region method."""
    # TOTEST use fixture for assembly graph
    asm_graph = AssemblyGraph(
        _IR_UN_SOL_REGMAP,
        _IR_UN_SOL_REGCTG_F,
    )
    # TOTEST use fixtures and composition
    assert list(asm_graph.oriented_contigs_of_region(0)) == [
        ('C0', FORWARD_INT),
        ('C1', REVERSE_INT),
    ]
    assert list(asm_graph.oriented_contigs_of_region(0, FORWARD_INT)) == [
        ('C0', FORWARD_INT),
        ('C1', REVERSE_INT),
    ]
    assert list(asm_graph.oriented_contigs_of_region(0, REVERSE_INT)) == [
        ('C1', FORWARD_INT),
        ('C0', REVERSE_INT),
    ]


# ---------------------------------------------------------------------------- #
#                              Rev_oriented_contig                             #
# ---------------------------------------------------------------------------- #
def test_rev_oriented_contig():
    """Test rev_oriented_contig function."""
    assert rev_oriented_contig(('0', FORWARD_INT)) == ('0', REVERSE_INT)
    assert rev_oriented_contig(('3', REVERSE_INT)) == ('3', FORWARD_INT)


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
def read_region_paths(region_paths_file: Path) -> Iterator[list[IndOrT]]:
    """Read region paths from file.

    Parameters
    ----------
    region_paths_file : Path
        Region paths file path

    Yields
    ------
    list of IndOrT
        Region path
    """
    # REFACTOR API function?
    with open(region_paths_file, 'r', encoding='utf-8') as regpaths_in:
        for line in regpaths_in:
            region_path = []
            l_regindor = line.split()
            k = 0
            while k < len(l_regindor) - 1:
                region_path.append(
                    (
                        IndexT(l_regindor[k]),
                        STR_ORIENT[l_regindor[k + 1]],  # type: ignore
                    ),
                )
                k += 2
            yield region_path


def read_oriented_contig_paths(oriented_contig_paths_file: Path) -> (
        Iterator[list[OrCT]]):
    """Read region paths from file.

    Parameters
    ----------
    oriented_contig_paths_file : Path
        Region paths file path

    Yields
    ------
    list of OrCT
        Oriented contig path
    """
    # REFACTOR API function?
    with open(oriented_contig_paths_file, 'r', encoding='utf-8') as regpaths_in:
        for line in regpaths_in:
            oriented_contig_path = []
            l_orc = line.split()
            k = 0
            while k < len(l_orc) - 1:
                oriented_contig_path.append(
                    (
                        l_orc[k],
                        STR_ORIENT[l_orc[k + 1]],  # type: ignore
                    ),
                )
                k += 2
            yield oriented_contig_path
