#!/bin/bash

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
import stat

import maelas.parser   as parser
import maelas.generate as generate

from pymatgen.core import Lattice, Structure
from pymatgen.transformations.standard_transformations import ConventionalCellTransformation,DeformStructureTransformation
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.io.vasp import Poscar
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

class run:

  def __init__(self,args):
        self.args = args
  
  
  def gen(self):

        
        generator = generate.VASP(self.args)
        structure0 = Structure.from_file(self.args.pos[0])
        generator.poscar2()
        generator.incar()
    
        sym1 = float(self.args.sympre[0])
        sym2 = float(self.args.symang[0])
    
        aa = SpacegroupAnalyzer(structure0,symprec=sym1, angle_tolerance=sym2)
        
        if self.args.noconv == False:
          structure1 = aa.get_conventional_standard_structure(international_monoclinic=True)
          bb = ConventionalCellTransformation(symprec=sym1, angle_tolerance=sym2, international_monoclinic=True)
          structure2 = bb.apply_transformation(structure1)
          
        
        if self.args.noconv == True:
          structure2 = structure0

        # Convention: lattice vector a1 along x-axis
        angle = -math.pi*(60.0/180.0)
        dd = DeformStructureTransformation(deformation=((math.cos(angle), math.sin(angle), 0), (-math.sin(angle), math.cos(angle), 0), (0, 0, 1)))
        structure2b = dd.apply_transformation(structure2)


        for i in range(int(self.args.ndist[0])):


            strain1 = - float(self.args.strain[0])+2*(float(self.args.strain[0])/(float(self.args.ndist[0])-1))*i

            print("strain", strain1)


         #Generation POSCAR file

        #b_21

            a1 = 1.0 + 0.5*strain1
            a2 = 1.0 + 0.5*strain1
            a3 = 1.0
            dd = DeformStructureTransformation(deformation=((a1, 0, 0), (0, a2, 0), (0, 0, a3)))
            structure3 = dd.apply_transformation(structure2b)
            pos_name = "POSCAR_1_" + str(i+1)

            structure33 = Poscar(structure3)
            structure33.write_file(filename = pos_name,significant_figures=16)

        #b_22

            
            a1 = 1.0
            a2 = 1.0
            a3 = 1.0 + strain1
            dd = DeformStructureTransformation(deformation=((a1, 0, 0), (0, a2, 0), (0, 0, a3)))
            structure3 = dd.apply_transformation(structure2b)
            pos_name2 = "POSCAR_2_" + str(i+1)

            structure33 = Poscar(structure3)
            structure33.write_file(filename = pos_name2,significant_figures=16)

        #b_3


            a1 = 1.0 + 0.5*strain1
            a2 = 1.0 - 0.5*strain1
            a3 = 1.0
            dd = DeformStructureTransformation(deformation=((a1, 0, 0), (0, a2, 0), (0, 0, a3)))
            structure3 = dd.apply_transformation(structure2b)
            pos_name3 = "POSCAR_3_" + str(i+1)

            structure33 = Poscar(structure3)
            structure33.write_file(filename = pos_name3,significant_figures=16)

        #b_4


            
            a11 = 1.0
            a12 = 0.0
            a13 = strain1
            a21 = 0.0
            a22 = 1.0
            a23 = 0.0
            a31 = strain1
            a32 = 0.0
            a33 = 1.0

            cc = DeformStructureTransformation(deformation=((a11, a12, a13), (a21, a22, a23), (a31, a32, a33)))
            structure4 = cc.apply_transformation(structure2b)
            pos_name4 = "POSCAR_4_" + str(i+1)

            structure44 = Poscar(structure4)
            structure44.write_file(filename = pos_name4,significant_figures=16)


        # b_13
                

            a11 = 1.0
            a12 = 0.0
            a13 = strain1
            a21 = 0.0
            a22 = 1.0
            a23 = 0.0
            a31 = strain1
            a32 = 0.0
            a33 = 1.0

            cc = DeformStructureTransformation(deformation=((a11, a12, a13), (a21, a22, a23), (a31, a32, a33)))
            structure5 = cc.apply_transformation(structure2b)
            pos_name5 = "POSCAR_5_" + str(i+1)

            structure55 = Poscar(structure5)
            structure55.write_file(filename = pos_name5,significant_figures=16)
            
            
            
        # b_43
                

            a11 = 1.0
            a12 = strain1
            a13 = 0.0
            a21 = strain1
            a22 = 1.0
            a23 = 0.0
            a31 = 0.0
            a32 = 0.0
            a33 = 1.0

            cc = DeformStructureTransformation(deformation=((a11, a12, a13), (a21, a22, a23), (a31, a32, a33)))
            structure6 = cc.apply_transformation(structure2b)
            pos_name6 = "POSCAR_6_" + str(i+1)

            structure66 = Poscar(structure6)
            structure66.write_file(filename = pos_name6,significant_figures=16)
            
            
            
            
            

        # INCAR_1_1 m=0,0,1

        path_inc_ncl_1_1 = 'INCAR_1_1'
        inc_ncl_1_1 = open(path_inc_ncl_1_1,'w')
        inc_ncl_list_1_1 = generator.inc_ncl_list[:]
        inc_ncl_list_1_1 += ['SAXIS = 0.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_1_1)):
            inc_ncl_1_1.write(str(inc_ncl_list_1_1[j]))

        inc_ncl_1_1.close()


    # INCAR_1_2 m=1,1,0

        path_inc_ncl_1_2 = 'INCAR_1_2'
        inc_ncl_1_2 = open(path_inc_ncl_1_2,'w')
        inc_ncl_list_1_2 = generator.inc_ncl_list[:]
        inc_ncl_list_1_2 += ['SAXIS = 1.0 1.0 0.0\n']

        for j in range(len(inc_ncl_list_1_2)):
            inc_ncl_1_2.write(str(inc_ncl_list_1_2[j]))

        inc_ncl_1_2.close()



    # INCAR_2_1 m=0,0,1

        path_inc_ncl_2_1 = 'INCAR_2_1'
        inc_ncl_2_1 = open(path_inc_ncl_2_1,'w')
        inc_ncl_list_2_1 = generator.inc_ncl_list[:]
        inc_ncl_list_2_1 += ['SAXIS = 0.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_2_1)):
            inc_ncl_2_1.write(str(inc_ncl_list_2_1[j]))

        inc_ncl_2_1.close()


    # INCAR_2_2 m=1,1,0

        path_inc_ncl_2_2 = 'INCAR_2_2'
        inc_ncl_2_2 = open(path_inc_ncl_2_2,'w')
        inc_ncl_list_2_2 = generator.inc_ncl_list[:]
        inc_ncl_list_2_2 += ['SAXIS = 1.0 1.0 0.0\n']

        for j in range(len(inc_ncl_list_2_2)):
            inc_ncl_2_2.write(str(inc_ncl_list_2_2[j]))

        inc_ncl_2_2.close()


        # INCAR_3_1 m=1,0,0

        path_inc_ncl_3_1 = 'INCAR_3_1'
        inc_ncl_3_1 = open(path_inc_ncl_3_1,'w')
        inc_ncl_list_3_1 = generator.inc_ncl_list[:]
        inc_ncl_list_3_1 += ['SAXIS = 1.0 0.0 0.0\n']

        for j in range(len(inc_ncl_list_3_1)):
            inc_ncl_3_1.write(str(inc_ncl_list_3_1[j]))

        inc_ncl_3_1.close()


    # INCAR_3_2 m=0,1,0

        path_inc_ncl_3_2 = 'INCAR_3_2'
        inc_ncl_3_2 = open(path_inc_ncl_3_2,'w')
        inc_ncl_list_3_2 = generator.inc_ncl_list[:]
        inc_ncl_list_3_2 += ['SAXIS = 0.0 1.0 0.0\n']

        for j in range(len(inc_ncl_list_3_2)):
            inc_ncl_3_2.write(str(inc_ncl_list_3_2[j]))

        inc_ncl_3_2.close()


        # INCAR_4_1 m=1,0,1

        path_inc_ncl_4_1 = 'INCAR_4_1'
        inc_ncl_4_1 = open(path_inc_ncl_4_1,'w')
        inc_ncl_list_4_1 = generator.inc_ncl_list[:]
        inc_ncl_list_4_1 += ['SAXIS = 1.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_4_1)):
            inc_ncl_4_1.write(str(inc_ncl_list_4_1[j]))

        inc_ncl_4_1.close()


        # INCAR_4_2 m=-1,0,1

        path_inc_ncl_4_2 = 'INCAR_4_2'
        inc_ncl_4_2 = open(path_inc_ncl_4_2,'w')
        inc_ncl_list_4_2 = generator.inc_ncl_list[:]
        inc_ncl_list_4_2 += ['SAXIS = -1.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_4_2)):
            inc_ncl_4_2.write(str(inc_ncl_list_4_2[j]))

        inc_ncl_4_2.close()



        # INCAR_5_1 m=1,1,0

        path_inc_ncl_5_1 = 'INCAR_5_1'
        inc_ncl_5_1 = open(path_inc_ncl_5_1,'w')
        inc_ncl_list_5_1 = generator.inc_ncl_list[:]
        inc_ncl_list_5_1 += ['SAXIS = 1.0 1.0 0.0\n']

        for j in range(len(inc_ncl_list_5_1)):
            inc_ncl_5_1.write(str(inc_ncl_list_5_1[j]))

        inc_ncl_5_1.close()


        # INCAR_5_2 m=-1,1,0

        path_inc_ncl_5_2 = 'INCAR_5_2'
        inc_ncl_5_2 = open(path_inc_ncl_5_2,'w')
        inc_ncl_list_5_2 = generator.inc_ncl_list[:]
        inc_ncl_list_5_2 += ['SAXIS = -1.0 1.0 0.0\n']

        for j in range(len(inc_ncl_list_5_2)):
            inc_ncl_5_2.write(str(inc_ncl_list_5_2[j]))

        inc_ncl_5_2.close()
        
        
        # INCAR_6_1 m=1,0,1

        path_inc_ncl_6_1 = 'INCAR_6_1'
        inc_ncl_6_1 = open(path_inc_ncl_6_1,'w')
        inc_ncl_list_6_1 = generator.inc_ncl_list[:]
        inc_ncl_list_6_1 += ['SAXIS = 1.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_6_1)):
            inc_ncl_6_1.write(str(inc_ncl_list_6_1[j]))

        inc_ncl_6_1.close()


        # INCAR_6_2 m=-1,0,1

        path_inc_ncl_6_2 = 'INCAR_6_2'
        inc_ncl_6_2 = open(path_inc_ncl_6_2,'w')
        inc_ncl_list_6_2 = generator.inc_ncl_list[:]
        inc_ncl_list_6_2 += ['SAXIS = -1.0 0.0 1.0\n']

        for j in range(len(inc_ncl_list_6_2)):
            inc_ncl_6_2.write(str(inc_ncl_list_6_2[j]))

        inc_ncl_6_2.close()





        

 # Derivation of magnetostriction coefficients:       

  def der(self):
  
        
        generator = generate.VASP(self.args)
        structure0 = Structure.from_file(self.args.pos[0])
        generator.poscar2()
    
        sym1 = float(self.args.sympre[0])
        sym2 = float(self.args.symang[0])
    
        aa = SpacegroupAnalyzer(structure0,symprec=sym1, angle_tolerance=sym2)
        
        if self.args.noconv == False:
          structure1 = aa.get_conventional_standard_structure(international_monoclinic=True)
          bb = ConventionalCellTransformation(symprec=sym1, angle_tolerance=sym2, international_monoclinic=True)
          structure2 = bb.apply_transformation(structure1)
          
        
        if self.args.noconv == True:
          structure2 = structure0

        # Convention: lattice vector a1 along x-axis
        angle = -math.pi*(60.0/180.0)
        dd = DeformStructureTransformation(deformation=((math.cos(angle), math.sin(angle), 0), (-math.sin(angle), math.cos(angle), 0), (0, 0, 1)))
        structure2b = dd.apply_transformation(structure2)
        
        
        nat = len(structure2b.species)
        vol = float(structure2b.volume)
        
        for j in range(1,7):

            for k in range(1,3):

                path_dat = "ene_" + str(j) + "_" + str(k) + ".dat"
                dat = open(path_dat,'w')


                for i in range(int(self.args.ndist[0])):
                    
                    strain1 = - float(self.args.strain[0])+2*(float(self.args.strain[0])/(float(self.args.ndist[0])-1))*i

                    #print("strain", strain1)


                    path_osz = "OSZICAR_" + str(j) + "_" + str(i+1) + "_" + str(k)
                    osz = open(path_osz,'r')
                    ene0 = osz.readlines()
                    ene1 = ene0[len(ene0)-2]
                    ene2 = ene1[11:32]

                    osz.close()

                    dat.write(repr(strain1))
                    dat.write('  ')
                    dat.write(str(ene2))
                    dat.write('\n')


                dat.close()


       # fitting and plot


        def K(x,a,b):
            return a*x+b


        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_21:")
        print("-------------------------")
        print(" ")
        print('Deformation x-direction and y-direction, spin1=[0,0,1] and spin2=[1,1,0]')
        print("")

        f = open('ene_1_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_1_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_1.png")
            print("")

        b21 = params[0][0]


        nn = int(self.args.ndist[0])+1
        if nn % 2 == 0:
            lli = int((nn-2)/2)
            mae001 = y[lli]




        #make figure dE_1.png

        fig = 'dE_1.png'
        spin1 = '0,0,1'
        spin2 = '1,1,0'
        tit = "Calculation of b21"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax1 = plt.gca()
        ax1.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5xx/2,  \u03B5yy/2"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()



        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_22:")
        print("-------------------------")
        print(" ")
        print('Deformation z-direction, spin1=[0,0,1] and spin2=[1,1,0]')
        print("")

        f = open('ene_2_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_2_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_2.png")
            print("")

        b22 = params[0][0]



        #make figure dE_2.png

        fig = 'dE_2.png'
        spin1 = '0,0,1'
        spin2 = '1,1,0'
        tit = "Calculation of b22"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax2 = plt.gca()
        ax2.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5zz"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()

        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_3:")
        print("-------------------------")
        print(" ")
        print('Deformation x-direction and y-direction, spin1=[1,0,0] and spin2=[0,1,0]')
        print("")

        f = open('ene_3_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_3_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_3.png")
            print("")

        b3 = params[0][0]


        nn = int(self.args.ndist[0])+1
        if nn % 2 == 0:
            lli = int((nn-2)/2)
            mae100 = y[lli]





        #make figure dE_3.png

        fig = 'dE_3.png'
        spin1 = '1,0,0'
        spin2 = '0,1,0'
        tit = "Calculation of b3"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax3 = plt.gca()
        ax3.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5xx/2"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()

        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_4:")
        print("-------------------------")
        print(" ")
        print('Deformation xz-direction, spin1=[1,0,1] and spin2=[-1,0,1]')
        print("")

        f = open('ene_4_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_4_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_4.png")
            print("")

        b4 = 0.5*params[0][0]


        #make figure dE_4.png

        fig = 'dE_4.png'
        spin1 = '1,0,1'
        spin2 = '-1,0,1'
        tit = "Calculation of b4"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax4 = plt.gca()
        ax4.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5xz"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()


        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_14:")
        print("-------------------------")
        print(" ")
        print('Deformation xz-direction, spin1=[1,1,0] and spin2=[-1,1,0]')
        print("")

        f = open('ene_5_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_5_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_5.png")
            print("")

        b14 = 0.5*params[0][0]

        #make figure dE_5.png

        fig = 'dE_5.png'
        spin1 = '1,1,0'
        spin2 = '-1,1,0'
        tit = "Calculation of b14"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax4 = plt.gca()
        ax4.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5xz"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()

        print("")
        print("Fit of linear function f(x)=A*x+B to energy vs strain")
        print("")
        print("-------------------------")
        print("Calculation of b_34:")
        print("-------------------------")
        print(" ")
        print('Deformation xy-direction, spin1=[1,0,1] and spin2=[-1,0,1]')
        print("")

        f = open('ene_6_1.dat','r')
        l = f.readlines()
        f.close

        x = []
        y = []
        for i in l:
            x.append(float(i.split()[0]))
            y.append(float(i.split()[1]))

        x = np.array(x)
        y = np.array(y)
        
        
        f2 = open('ene_6_2.dat','r')
        l2 = f2.readlines()
        f2.close

        x2 = []
        y2 = []
        for i in l2:
            x2.append(float(i.split()[0]))
            y2.append(float(i.split()[1]))

        x2 = np.array(x2)
        y2 = np.array(y2)
        

        params = curve_fit(K, x, y-y2)

        print("Fitting parameters:")
        print("A =", params[0][0], ", B =", params[0][1])

        r_squared = r2_score(y-y2, K(x,params[0][0],params[0][1]))
        print("R-squared =", r_squared)
        print("")

        if r_squared < 0.98:
            print("WARNING!! R-squared is lower than 0.98. Check figure dE_6.png")
            print("")

        b34 = 0.5*params[0][0]

        #make figure dE_6.png

        fig = 'dE_6.png'
        spin1 = '1,0,1'
        spin2 = '-1,0,1'
        tit = "Calculation of b34"

        plt.plot(x, (y-y2)*1e6, 'o', label='data')
        plt.plot(x, K(x, params[0][0],params[0][1])*1e6, 'r-', label='fit')
        plt.legend()
        ax4 = plt.gca()
        ax4.xaxis.set_major_locator(plt.MaxNLocator(5))

        ylabel ='E[' + str(spin1) + '] - E['+ str(spin2) + '] (\u03BCeV)'
        plt.ylabel(ylabel)
        label = "Strain \u03B5xy"
        plt.xlabel(label)
        plt.title(tit)
        plt.tight_layout(pad=6, h_pad=None, w_pad=None, rect=None)
        plt.ticklabel_format(axis='both', style='plain', useOffset=False, useMathText=True)
        plt.savefig(fig)
        plt.close()       
        
        
        print(" ")
        print("----------------------------------------------")
        print("Anisotropic magnetoelastic constants:")
        print("----------------------------------------------")
        print(" ")

        
            
        print(" ")
        print("Using the convention in reference P. Nieves et al., Comput. Phys. Commun. 264, 107964 (2021):")
        print(" ")
        print("b21 =", b21,u' eV')
        print(" ")
        print("b22 =", b22,u' eV')
        print(" ")
        print("b3 =", b3,u' eV')
        print(" ")
        print("b4 =", b4,u' eV')
        print(" ")
        print("b13 =", b14,u' eV')
        print(" ")
        print("b34 =", b34,u' eV')
        print(" ")
        print("b21 =", b21/nat,u' eV/atom')
        print(" ")
        print("b22 =", b22/nat,u' eV/atom')
        print(" ")
        print("b3 =", b3/nat,u' eV/atom')
        print(" ")
        print("b4 =", b4/nat,u' eV/atom')
        print(" ")
        print("b13 =", b14/nat,u' eV/atom')
        print(" ")
        print("b34 =", b34/nat,u' eV/atom')
        print(" ")
        print("b21 =", b21/vol,u' eV/A^3')
        print(" ")
        print("b22 =", b22/vol,u' eV/A^3')
        print(" ")
        print("b3 =", b3/vol,u' eV/A^3')
        print(" ")
        print("b4 =", b4/vol,u' eV/A^3')
        print(" ")
        print("b13 =", b14/vol,u' eV/A^3')
        print(" ")
        print("b34 =", b34/vol,u' eV/A^3')
        print(" ")
        print("b21 =", (b21/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ")
        print("b22 =", (b22/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ")
        print("b3 =", (b3/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ")
        print("b4 =", (b4/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ")
        print("b13 =", (b14/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ")
        print("b34 =", (b34/vol)*1.602176565e-19*1e30*1e-6 ,u' MPa')
        print(" ") 
            
        bani1 = (b21/vol)*1.602176565e-19*1e30*1e-6
        bani2 = (b22/vol)*1.602176565e-19*1e30*1e-6
        bani3 = (b3/vol)*1.602176565e-19*1e30*1e-6
        bani4 = (b4/vol)*1.602176565e-19*1e30*1e-6
        bani5 = (b14/vol)*1.602176565e-19*1e30*1e-6
        bani6 = (b34/vol)*1.602176565e-19*1e30*1e-6
        
        path_inc_std = 'MAGANI'
        inc_std = open(path_inc_std,'w')
        inc_std.write(str(bani1))
        inc_std.write('\n')
        inc_std.write(str(bani2))
        inc_std.write('\n')
        inc_std.write(str(bani3))
        inc_std.write('\n')
        inc_std.write(str(bani4))
        inc_std.write('\n')
        inc_std.write(str(bani5))
        inc_std.write('\n')
        inc_std.write(str(bani6))
        inc_std.close()
        
        if nn % 2 == 0:         
                print("----------------------------------------------")
                print("Magnetocrystalline anisotropy energy:")
                print("----------------------------------------------")
                print(" ")
                print("These energies correspond to the central points in the data files ene_1_1.dat and ene_3_1.dat:")
                print(" ")
                print("E(0,0,1) = ",mae001," eV")
                print(" ")
                print("E(1,0,0) = ",mae100," eV")
                print(" ")
                print("E(1,0,0) - E(0,0,1) = ",(mae100 - mae001)*1e6,u'x 10\u207B\u2076 eV')
                print(" ")
                print("[E(1,0,0) - E(0,0,1)]/Natom = ",((mae100 - mae001)/nat)*1e6,u'x 10\u207B\u2076 eV/atom')


        if self.args.delas == True:

                print(" ")
                print(" ")
                print("----------------------------------------------")
                print("Calculation of magnetostrictive coefficients:")
                print("----------------------------------------------")
                print(" ")
                print("Reading the elastic tensor file =", str(self.args.elas[0]))
                print(" ")




                elasdat = open(self.args.elas[0],'r')
                elasline = elasdat.readlines()
                elasline0 = elasline[2]
                elasline1 = elasline[4]
                elasline2 = elasline[5]
                elasline3 = elasline[7]
                c11 = float(elasline0[0:8])
                c12 = float(elasline0[8:16])
                c13 = float(elasline0[16:24])
                c14 = float(elasline0[24:32])
                c33 = float(elasline1[16:24])
                c44 = float(elasline2[24:32])
                c66 = float(elasline3[40:48])

                elasdat.close()
                
                
                bb21 = (b21/vol)*1.602176565e-19*1e30*1e-9
                
                bb22 = (b22/vol)*1.602176565e-19*1e30*1e-9
                
                bb3 = (b3/vol)*1.602176565e-19*1e30*1e-9
                
                bb4 = (b4/vol)*1.602176565e-19*1e30*1e-9
                
                bb14 = (b14/vol)*1.602176565e-19*1e30*1e-9
                
                bb34 = (b34/vol)*1.602176565e-19*1e30*1e-9


                lambda_alpha_1_2 = (bb22*c13-bb21*c33)/(-2.0*c13**2.0+(c11+c12)*c33)

                lambda_alpha_2_2 = (-bb22*(c11+c12)+2.0*bb21*c13)/(-2.0*c13**2.0+(c11+c12)*c33)

                lambda_gamma_1 = (0.5*c14*bb14-0.5*c44*bb3)/(0.5*c44*(c11-c12)-c14**2.0)

                lambda_gamma_2 = (-0.5*bb4*(c11-c12)+bb34*c14)/(0.5*c44*(c11-c12)-c14**2.0)
                
                lambda_1_2 = (c14*bb4-c44*bb34)/(0.5*c44*(c11-c12)-c14**2.0)
                
                lambda_2_1 = (-0.5*bb14*(c11-c12)+bb3*c14)/(0.5*c44*(c11-c12)-c14**2.0)



                print("c11 =", str(c11), 'GPa')
                print(" ")
                print("c12 =", str(c12), 'GPa')
                print(" ")
                print("c13 =", str(c13), 'GPa')
                print(" ")
                print("c14 =", str(c14), 'GPa')
                print(" ")
                print("c33 =", str(c33), 'GPa')
                print(" ")
                print("c44 =", str(c44), 'GPa')
                print(" ")
                print("c66 =", str(c66), 'GPa')
                print(" ")
                print("Warning: If these elastic constants are not the same as in the input elastic tensor file", str(self.args.elas[0]),", then check that the format of the elastic tensor is exactly the same as in the standard output file ELADAT generated by AELAS code (see Example folder)")
                print(" ")
                print(" ")
                print(" ")
                print("----------------------------------------------")
                print("Anisotropic magnetostriction coefficients:")
                print("----------------------------------------------")
                print(" ")
                print("Using the convention in reference J.R. Cullen et al., in Materials, Science and Technology (VCH Publishings, 1994), pp.529-565:")
                print(" ")
                print("\u03BB \u03B11,2  =", lambda_alpha_1_2*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("\u03BB \u03B12,2 =", lambda_alpha_2_2*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("\u03BB \u02631 =", lambda_gamma_1*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("\u03BB \u02632 =", lambda_gamma_2*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("\u03BB 12 =", lambda_1_2*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("\u03BB 21 =", lambda_2_1*1e6,u'x 10\u207B\u2076')
                print(" ")
                print(" ")
                print("/////////////////////")
                print("Spontaneous volume magnetostriction (anisotropic contribution):")
                print("/////////////////////")
                print(" ")
                print("Trigonal crystal with easy axis (ferromagnetic state with equal domains along all equivalent easy directions): ")
                print(" ")
                print("\u03C9_s^ani =", ((4.0/3.0)*lambda_alpha_1_2+(2.0/3.0)*lambda_alpha_2_2)*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("......................... ")
                print(" ")
                print("Trigonal crystal with easy plane (ferromagnetic state with equal domains along all equivalent easy directions): ")
                print(" ")
                print("\u03C9_s^ani =", (-(2.0/3.0)*lambda_alpha_1_2-(1.0/3.0)*lambda_alpha_2_2)*1e6,u'x 10\u207B\u2076')
                print(" ")
                print("/////////////////////")
                print("Polycrystal (uniform stress approximation):")
                print("/////////////////////")
                print(" ")
                print(" ")
                print("Trigonal crystal with easy axis (reference demagnetized state with equal domains along all easy directions): ")
                print(" ")
                print("\u03BE =", 1e6*((4.0/15.0)*lambda_alpha_1_2+(1.0/15.0)*lambda_alpha_2_2-(2.0/15.0)*lambda_gamma_1-(1.0/15.0)*lambda_gamma_2-(1.0/3.0)*(2.0*lambda_alpha_1_2+lambda_alpha_2_2)),u'x 10\u207B\u2076')
                print(" ")
                print("\u03B7 =", 1e6*(-(2.0/15.0)*lambda_alpha_1_2+(2.0/15.0)*lambda_alpha_2_2+(2.0/5.0)*lambda_gamma_1+(1.0/5.0)*lambda_gamma_2),u'x 10\u207B\u2076')
                print(" ")
                print("......................... ")
                print(" ")
                print("Trigonal crystal with easy plane (reference demagnetized state with equal domains along all easy directions): ")
                print(" ")
                print("\u03BE =", 1e6*((4.0/15.0)*lambda_alpha_1_2+(1.0/15.0)*lambda_alpha_2_2-(2.0/15.0)*lambda_gamma_1-(1.0/15.0)*lambda_gamma_2),u'x 10\u207B\u2076')
                print(" ")
                print("\u03B7 =", 1e6*(-(2.0/15.0)*lambda_alpha_1_2+(2.0/15.0)*lambda_alpha_2_2+(2.0/5.0)*lambda_gamma_1+(1.0/5.0)*lambda_gamma_2),u'x 10\u207B\u2076')
                print(" ")
                print(" ") 

          
        
        