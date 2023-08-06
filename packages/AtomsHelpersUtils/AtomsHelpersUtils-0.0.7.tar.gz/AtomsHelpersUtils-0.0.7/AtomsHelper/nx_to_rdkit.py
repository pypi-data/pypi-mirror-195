# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 02:55:45 2023

@author: eccn3
"""

import networkx as nx

from AtomsHelper.utils import draw_surf_graph

from rdkit import Chem
from rdkit.Chem.rdmolops import FindAllSubgraphsOfLengthMToN
from rdkit.Chem.rdchem import BondType


from ase import formula
from ase.data import chemical_symbols
from ase.visualize import view

class rdkit_helper():
    def __init__(self, nx_graph = None, rdkit_mol = None, metal = 'Pt'):
        self.substrate = metal
        self.gen_m_g = None
        self.g = None
        
        metals = [i for i in chemical_symbols if i not in formula.non_metals]
        
        if nx_graph:
            gen_m_graph = 'M' in nx.get_node_attributes(nx_graph, 'element').values()
            if gen_m_graph: 
                self.gen_m_g = nx_graph
                self.gen_metal_assign()
            else:
                self.g = nx_graph
            
        self.mol = rdkit_mol
        

        self.rdkit_bond_chart = {0.: BondType.ZERO,
                                 0.5: BondType.SINGLE,
                                 1.: BondType.SINGLE,
                                 1.5: BondType.ONEANDAHALF,
                                 2.: BondType.DOUBLE,
                                 2.5: BondType.TWOANDAHALF,
                                 3.: BondType.TRIPLE, 
                                 3.5: BondType.THREEANDAHALF,
                                 }

    def gen_metal_assign(self):
        
        """
        If there exists a generalizes metal graph, assigns substrate element
        to generalized metal nodes
        
        In
        -------
        self: self.gen_m_g

        Returns
        -------
        self: self.g

        """
        
        if self.gen_m_g:
            G = self.gen_m_g.copy()
            
            for node in G.nodes():
                if G.nodes[node]['element'] =='M':
                    G.nodes[node]['element'] = self.substrate
            
            self.g = G
        else:
            print('No generalized metal graph')

    def nx_to_mol(self):
        
        """
        Converts networkx graph (self.g) into an rdkit mol
        Bonds are rounded, but fractional values are still kept via bond prop
        
        In
        -------
        self: self.g

        Returns
        -------
        self: self.mol

        """
        
        if not self.g:
            print('No applicable nx graph')
            
        else:
            
            G = self.g.copy()
            
            mol = Chem.RWMol()
            atomic_nums = nx.get_node_attributes(G, 'element')
            node_to_idx = {}
            edge_to_idx = {}
            for node in G.nodes():
                
                a=Chem.Atom(atomic_nums[node])
                idx = mol.AddAtom(a)
                mol.GetAtomWithIdx(idx).SetIntProp('nx_idx', int(node))
                node_to_idx[node] = idx
        
            bond_weight = nx.get_edge_attributes(G, 'weight')
            bond_length = nx.get_edge_attributes(G, 'distance')
            
            for edge in G.edges():
                
                first, second = edge
                ifirst = node_to_idx[first]
                isecond = node_to_idx[second]
                
                bond = bond_weight[first, second]
                bond_type = self.rdkit_bond_chart[float(round(bond*2)/2)]
                bond_distance = bond_length[first, second]
                
                mol.AddBond(ifirst, isecond, bond_type)
                edge_to_idx[first, second] = (ifirst, isecond)
                mol.GetBondBetweenAtoms(ifirst, isecond).SetDoubleProp('bond_index', bond_type)
                mol.GetBondBetweenAtoms(ifirst, isecond).SetDoubleProp('distance', bond_distance)
            
            self.mol = mol
            self.g_node_map = node_to_idx
            self.g_edge_map = edge_to_idx
            
            return mol


    def mol_to_nx(self, mol, bondids=None):
        """
        Straight up, Himaghna's function.
        rdkit mol to nx graph
        
        Parameters
        ----------
        mol: RDKIT molecule object
        bondids: tuple
            Bond-ids making the graph.
        Returns
        -------
            networkx Graph object.
        """
        g = nx.Graph()
        
        mol_idx = set()
        
        if not bondids:
            bondids = [i.GetIdx() for i in list(rh.mol.GetBonds())]
        
        for bondid in bondids:
            
            Bond = mol.GetBondWithIdx(bondid)
            
            bond_props = Bond.GetPropsAsDict()
            
            begin_atom_idx = Bond.GetBeginAtomIdx()
            end_atom_idx = Bond.GetEndAtomIdx()
            
            if begin_atom_idx not in mol_idx:
            
                g.add_node(begin_atom_idx,
                            atomic_number=(mol.GetAtomWithIdx(begin_atom_idx))
                                    .GetAtomicNum(),
                            element=(mol.GetAtomWithIdx(begin_atom_idx))
                                    .GetSymbol())
                
                mol_idx.add(begin_atom_idx)
                
            if end_atom_idx not in mol_idx:
                
                g.add_node(end_atom_idx,
                            atomic_number=(mol.GetAtomWithIdx(end_atom_idx))
                                    .GetAtomicNum(),
                            element=(mol.GetAtomWithIdx(end_atom_idx))
                                    .GetSymbol())
                mol_idx.add(begin_atom_idx)
            
            g.add_edge(begin_atom_idx, end_atom_idx,
                       **bond_props)

        return g


    def enumerate_subgraphs(self, min_=1, max_=4, useHs=True):
        
        """
        Enumerate subgraphs 
        
        In
        -------
        self: self.mol

        Returns
        -------
        self: self.subgraphs: tuple of a list of tuples

        """
        
        self.mol_subgraphs = FindAllSubgraphsOfLengthMToN(self.mol,
                                                      min = min_,
                                                      max = max_,
                                                      useHs = useHs)
        
        nx_subgraphs = []
        for i in self.mol_subgraphs:
            for j in i:
                nx_subgraphs.append(self.mol_to_nx(self.mol, j))
        self.nx_subgraphs = nx_subgraphs
        
        return nx_subgraphs    
        
    # def change_metal()
        
    def print_mol_atoms(self):
        
        """
        Returns self.mol atom properties
        
        In
        -------
        self: self.mol

        Returns
        -------
        print

        """
        
        if not self.mol:
            print('No rdkit mol')
            return
        else:
            for atom in self.mol.GetAtoms():
                print(atom.GetIdx(),
                      atom.GetAtomicNum(),
                      )
                
    def print_mol_bonds(self):
        
        """
        Returns self.mol bond properties
        
        In
        -------
        self: self.mol

        Returns
        -------
        print

        """
        if not self.mol:
            print('No rdkit mol')
            return
        else:
            for bond in self.mol.GetBonds():
                print(bond.GetBeginAtomIdx(),
                      bond.GetEndAtomIdx(),
                      bond.GetPropsAsDict())

def mol_with_atom_index(mol):
    for atom in mol.GetAtoms():
        atom.SetAtomMapNum(atom.GetIdx())
    return mol
    
if __name__ == '__main__':
    import pickle as pk
    
    from rdkit.Chem.Draw import IPythonConsole
    from rdkit.Chem import Draw
    IPythonConsole.ipython_useSVG=True
    
    graph = pk.load(open('Examples/nx_mol_helper/OCH3-Pt-hol.pk', 'rb'))
    rh = rdkit_helper(nx_graph = graph)
    rh.nx_to_mol()
    rh.enumerate_subgraphs(useHs=True)
    rh.print_mol_bonds()
    graph_return = rh.mol_to_nx(rh.mol)
    draw_surf_graph(graph_return, cutoff= None, edge_labels = True, edge_label_type = 'bond_index')
    mol_with_atom_index(rh.mol)
