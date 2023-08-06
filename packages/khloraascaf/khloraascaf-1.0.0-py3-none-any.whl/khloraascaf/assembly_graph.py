# -*- coding=utf-8 -*-

"""Module for assembly graph and multiple solution generator."""


from collections.abc import Iterable, Iterator
from pathlib import Path
from queue import LifoQueue

from bitarray import bitarray
from revsymg.graphs import RevSymGraph
from revsymg.index_lib import (
    FORWARD_INT,
    IND,
    ORIENT_REV,
    EIndOrIndT,
    IndexT,
    IndOrT,
    OrT,
)

from khloraascaf.outputs import (
    ORC_ID_IND,
    ORC_OR_IND,
    OrCT,
    read_contigs_of_regions,
    read_map_of_regions,
)


# ============================================================================ #
#                                     CLASS                                    #
# ============================================================================ #
class AssemblyGraph():
    """Khloraascaf assembly graph."""

    def __init__(self, map_of_regions_path: Path,
                 contigs_of_regions_path: Path):
        """The Initializer."""
        self.__graph: RevSymGraph = RevSymGraph()
        self.__regions_contigs: list[list[OrCT]] = []
        self.__read_regions_contigs(contigs_of_regions_path)
        self.__add_regions_links(map_of_regions_path)

    def all_region_paths(self) -> Iterator[list[IndOrT]]:
        """Iterate over all the paths of oriented regions.

        Yields
        ------
        list of IndOrT
            Path of oriented regions
        """
        edges = self.__graph.edges()

        used_edges: bitarray = bitarray('0') * (
            edges.biggest_edge_index() + 1)

        starter = (0, FORWARD_INT)

        path: list[IndOrT] = [starter]
        eind_path: list[IndexT] = []
        lifo: LifoQueue[EIndOrIndT] = LifoQueue()

        for v, e_ind in edges.succs(starter):
            lifo.put((starter, v, e_ind))

        while not lifo.empty():
            _, v, e_ind = lifo.get()
            path.append(v)
            eind_path.append(e_ind)
            used_edges[e_ind] = True

            vw_not_used: list[EIndOrIndT] = []
            for w, f_ind in edges.succs(v):
                if w[IND] != starter[IND] and not used_edges[f_ind]:
                    vw_not_used.append((v, w, f_ind))

            if vw_not_used:
                for v, w, f_ind in vw_not_used:
                    lifo.put((v, w, f_ind))
            else:
                # FIXME: not sure all the edges were used!
                #   * come back to the idea of number of zero-degrees?
                yield path
                #
                # Back to the first branching vertex
                #
                if not lifo.empty():
                    branch_src, branch_succ, branch_eind = lifo.get()
                    lifo.put((branch_src, branch_succ, branch_eind))
                    while path[-1] != branch_src:
                        path.pop()
                        used_edges[eind_path.pop()] = False

    def all_oriented_contig_paths(self) -> Iterator[list[OrCT]]:
        """Iterate over all the paths of oriented contigs.

        Yields
        ------
        list of IndOrT
            Path of oriented contigs
        """
        for region_path in self.all_region_paths():
            oriented_contig_path: list[OrCT] = []
            for reg_ind, reg_or in region_path:
                for orc in self.oriented_contigs_of_region(reg_ind, reg_or):
                    oriented_contig_path.append(orc)
            yield oriented_contig_path

    def region_path_to_oriented_contigs(
            self, region_path: Iterable[IndOrT]) -> Iterator[OrCT]:
        """Iterate over the oriented contigs of a given region path.

        Parameters
        ----------
        region_path : iterable of IndOrT
            Path of oriented regions

        Yields
        ------
        OrCT
            Oriented contig
        """
        for reg_ind, reg_or in region_path:
            yield from self.oriented_contigs_of_region(reg_ind, reg_or)

    # ~*~ Getter ~*~

    def revsymg(self) -> RevSymGraph:
        """Return the reverse symmetric graph associated.

        Returns
        -------
        RevSymGraph
            Reverse symmetric graph
        """
        return self.__graph

    def oriented_contigs_of_region(self, region_ind: IndexT,
                                   orientation: OrT = FORWARD_INT) -> (
            Iterator[OrCT]):
        """Iterate over oriented contigs of the oriented region.

        Parameters
        ----------
        region_ind : IndexT
            Region's index
        orientation : OrT, optional
            Region's orientation, by default FORWARD_INT

        Yields
        ------
        OrCT
            Oriented contig of the oriented region
        """
        if orientation == FORWARD_INT:
            yield from self.__regions_contigs[region_ind]
        else:
            for oriented_contig in reversed(self.__regions_contigs[region_ind]):
                yield rev_oriented_contig(oriented_contig)

    # ~*~ Private ~*~

    def __read_regions_contigs(self, contigs_of_regions_path: Path):
        """Extract the oriented contigs for each region.

        Parameters
        ----------
        contigs_of_regions_path : Path
            List of oriented contigs for each region
        """
        vertices = self.__graph.vertices()
        for region_ind, oriented_contigs in read_contigs_of_regions(
                contigs_of_regions_path):
            assert region_ind == vertices.add()
            self.__regions_contigs.append(oriented_contigs)

    def __add_regions_links(self, map_of_regions_path: Path):
        """Add regions links from map of regions.

        Parameters
        ----------
        map_of_regions_path : Path
            Map of regions
        """
        edges = self.__graph.edges()
        reg_indor_iter = read_map_of_regions(map_of_regions_path)
        start_indor = next(reg_indor_iter)
        u_indor = start_indor
        for v_indor in reg_indor_iter:
            edges.add(u_indor, v_indor)
            u_indor = v_indor
        edges.add(u_indor, start_indor)


# ============================================================================ #
#                                   FUNCTIONS                                  #
# ============================================================================ #
def rev_oriented_contig(oriented_contig: OrCT) -> OrCT:
    """Return the reverse of the oriented contig.

    Parameters
    ----------
    oriented_contig : OrCT
        Oriented contig

    Returns
    -------
    OrCT
        Its reverse
    """
    return oriented_contig[ORC_ID_IND], ORIENT_REV[oriented_contig[ORC_OR_IND]]
