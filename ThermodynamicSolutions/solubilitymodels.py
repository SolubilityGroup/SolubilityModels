import sys 
import pandas as pd
import numpy as np
from IPython.display import display, Math, Latex, Markdown,HTML
from IPython.core.display import display, HTML
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from math import ceil
import  tikzplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
from matplotlib import rcParams
from matplotlib import cm 

import os
import platform
import subprocess


import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)


def data_upload(name):
    nombre = name
    uploaded = files.upload()
    for fn in uploaded.keys():
        nombre = fn
    return nombre


def generate_pdf(filename_tex):

    # TeX source filename
    tex_filename = filename_tex+".tex"
    filename, ext = os.path.splitext(tex_filename)
    # the corresponding PDF filename
    pdf_filename = filename + '.pdf'

    # compile TeX file
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_filename])

    # check if PDF is successfully generated
    if not os.path.exists(pdf_filename):
        raise RuntimeError('PDF output not found')

    # open PDF with platform-specific command
    if platform.system().lower() == 'darwin':
        subprocess.run(['open', pdf_filename])
    elif platform.system().lower() == 'windows':
        os.startfile(pdf_filename)
    elif platform.system().lower() == 'linux':
        subprocess.run(['xdg-open', pdf_filename])
    else:
        raise RuntimeError('Unknown operating system "{}"'.format(platform.system()))

    if entorno == "/usr/bin/python3" :
        path = "/content/"+ filename_tex +".pdf"
        files.download(path)
    else:
        path = filename_tex +".pdf"


def environment_table(file_name):

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass{article}\n\\usepackage{booktabs}\n\\usepackage{array}\n\\usepackage{makecell}\n\\usepackage{graphicx}\n\\begin{document}\n"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def environment_graph(file_name):

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass[tikz]{standalone}\n\\usepackage{pgfplots}\n\\begin{document}\n"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)

def environment_graph_apart(file_name,cols,rows):

    with open(file_name,'r') as read_file:
        lines = read_file.readlines()

    currentLine = 1
    with open(file_name,'w') as write_file:
        for line in lines:
            if currentLine < 7:
                pass
            else:
                write_file.write(line)
        
            currentLine += 1

    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    line = "\\documentclass[tikz]{standalone}\n\\usepackage{pgfplots}\n\\usepgfplotslibrary{groupplots}\n\\pgfkeys{/pgf/number format/.cd,fixed,precision=3}\n\\pgfplotsset{compat=1.3,every axis/.append style={scale only axis,height=5.5cm}}\n\\begin{document}\n\\begin{tikzpicture}\n\\definecolor{darkgray176}{RGB}{176,176,176}\n\\begin{groupplot}[group style={group size="+str(cols)+ " by " + str(rows)+", horizontal sep=2cm, vertical sep=3cm}]"

    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

    text_to_append = "\\end{document}"

    """Append given text as a new line at the end of file"""
    # Open the file in append & read mode ('a+')
    with open(file_name, "a+") as file_object:
        # Move read cursor to the start of file.
        file_object.seek(0)
        # If file is not empty then append '\n'
        data = file_object.read(100)
        if len(data) > 0:
            file_object.write("\n")
        # Append text at the end of file
        file_object.write(text_to_append)


class dataset:

    """
    dataset
    =======
    ### `dataset("archive path")` or `dataset()`
    -------------------------------------------------------------------------------
    Class to upload the dataset according to the format of the standard table in 
    extension "xlsx" or "csv", receives a path or url as argument.

    ------------------------------------------------------------------------------
    # Examples
    The data must be loaded in the standard table format in the following ways:
    - Examples for loading standard data table from a path in the format "xlsx" or "csv":
    >>> data = dataset("/content/SMR-MeCN-MeOH.csv")
    >>> data = dataset("/content/SMR-MeCN-MeOH.xlsx")

    - Example for loading standard data table from a url in Github:
    >>> data = dataset("https://raw.githubusercontent.com/SMR-MeCN-MeOH.csv")

    - Example for loading standard data table from the pc in Google Colaboratory:
    >>> data = dataset()

    - Link to see the standard table: https://da.gd/CAx7m
    """

    def __init__(self,url=""):
        global URL
        global entorno
        self.url = url
        entorno = str(sys.executable)
        if self.url == ""  and entorno == "/usr/bin/python3" :     
            name = data_upload(self.url)
            URL= "/content/"+ name
        else:
            URL =self.url
       
    @property
    def show(self):
        """Method to show the data loaded as a dataframe.
        """
        L = URL.split(".")

        if L[-1]=="csv":
            df = pd.read_csv(URL)

        if L[-1]=="xlsx":
            df = pd.read_excel(URL)

        return df
    
    
    @property
    def temperature_values(self):

        """Method to show the values of the temperatures in a dataframe.
        """

        df = self.show
        if "x1" in df.columns or "x2" in df.columns:
            temp = df.drop(['x1',"x2"], axis=1).columns[1:]
        else:
            temp = df.columns[1:]
        return pd.DataFrame({"T":temp})
    
    @property
    def mass_fractions(self):

        """Method to show the values of the mass fractions in a dataframe.
        """
        df = self.show
        fm = df["w1"]
        df_fm = pd.DataFrame({"w1":fm})
        return df_fm

    
    def experimental_values(self,scale = 0,download_format = "None"):

        """
        experimental_values
        ===================
        ### `experimental_values(scale=0,download_format="None")`
        -------------------------------------------------------------------------------
        Method to show and download in different formats the dataframe experimental values 
        of the model, the experimental mole fractions of solubility can be multiplied 
        by a power of ten.

        ------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = modified_apelblat(data,Tf)
        >>> model_name.experimental_values(scale=0,download_format="xlsx")

        >>> data.experimental_values(scale=3,download_format="tex") #other way

        -------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Parameters 
        The explanation of the parameters of this method are presented below:
        - ### scale: int, optional
        Option to indicate the exponent of the power of 10. All experimental mole
        fractions are multiplied by this power .e.g. scale = 3 multiply the mole 
        fractions by the power 10^3. Default is scale=0.
        - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
        Option to download the table of experimental values in the chosen format,
        excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
        """

        L = URL.split(".")

        if L[-1]=="csv":
            df = pd.read_csv(URL)
        if L[-1]=="xlsx":
            df = pd.read_excel(URL)


        if "x1" in df.columns or "x2" in df.columns:
            df_ev = df.drop(['x1',"x2"], axis=1)
        else:
            df_ev = df

  
        name_archi = URL.split("/")[-1].split(".")[-2]

        cols = df_ev.columns.astype(str).tolist()

        for i in cols[1:]:
            df_ev[i] = 10**(scale)* df_ev[i]

        nombre ="experimental values"
        
        extension = download_format
        namecols=["$w_1$"]+["$"+i+"$" for i in cols[1:]]


        def f1(x):return '%1.2f' % x

        if scale != 0:
            def f2(x):return '%1.2f' % x
        else:
            def f2(x):return '%1.5f' % x

        if extension == "tex":     
            if entorno == "/usr/bin/python3":
                url_7 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_ev.to_latex(url_7,index=False,column_format= len(cols)*"c", formatters=[f1]+(len(cols)-1)*[f2],header=namecols,escape =False)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"."+extension
                df_ev.to_latex(url_7,index=False,column_format= len(cols)*"c", formatters=[f1]+(len(cols)-1)*[f2],header=namecols,escape =False)

            environment_table(url_7)
            generate_pdf(nombre + "-"+ name_archi)

        if extension == "xlsx":  
            if entorno == "/usr/bin/python3" :
                url_7 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_ev.to_excel(url_7,sheet_name=nombre)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"."+extension
                df_ev.to_excel(url_7,sheet_name=nombre)

        if extension == "csv":   
            if entorno == "/usr/bin/python3":
                url_7 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_ev.to_csv(url_7)
                files.download(url_7)
            else:
                url_7 = nombre + "-"+ name_archi +"."+extension
                df_ev.to_csv(url_7)

        return df_ev


    def molar_fractions(self,mf):
        
        """Method to show the values the molar fractions in a dataframe.
        """
        if mf == "x1":
            df_mf = print("Does not exist mole fraction for "+ mf)
        if mf == "x2":
            df_mf = print("Does not exist mole fraction for "+ mf)
        if mf == "x3":
            df_mf = self.experimental_values()
        return df_mf

class model:

    """
    model
    =====
    ### `model.mame_model(dataset,Tf,ΔHf)`
    --------------------------------------------------------------------------------------
    Class to choose the solubility model for a dataset with melting temperature Tf 
    and enthalpy of fusion ΔHf.

    -------------------------------------------------------------------------------------
    # Examples
    >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
    >>> model_apelblat = model.modified_apelblat(data)

    ----------------------------------------------------------------------------------------
    ##  Solubility models
    The solubility models loaded into the library in this version are presented
    below with their respective parameters:
    >>> model.modified_apelblat(data)
    >>> model.vant_hoff(data)
    >>> model.vant_hoff_yaws(data)
    >>> model.modified_wilson(data)
    >>> model.buchowski_ksiazaczak(data,Tf) #λh model
    >>> model.NRTL(data,Tf,ΔHf)
    >>> model.wilson(data,Tf,ΔHf)
    >>> model.weibull(data,Tf,ΔHf)
    """

    def __init__(self):
        self.modified_apelblat    = self.modified_apelblat()
        self.vant_hoff            = self.vant_hoff()
        self.vant_hoff_yaws       = self.vant_hoff_yaws()
        self.modified_wilson      = self.modified_wilson()
        self.buchowski_ksiazaczak = self.buchowski_ksiazaczak()
        self.NRTL                 = self.NRTL()
        self.wilson               = self.wilson()
        self.weibull              = self.weibull()

#CLASE PARA EL MODELO DE SOLUBILIDAD APELBLAT MODIFICADO

    class modified_apelblat(dataset):

        """
        Modified Apelblat Model
        ==========================
        ### `model.modified_apelblat(dataset)`
        -------------------------------------------------------------------------------------------------
        Class of the Modified Apelblat model, receives as argument 
        a dataset for find the model parameters, calculated values and 
        make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.modified_apelblat(data)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(method="lm", p0 =[1,1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format='None')
        >>> model_name.values(method="lm", p0 =[1,1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(method="lm", p0 =[1,1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(method="lm",p0 =[1,1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(method="lm", p0 =[1,1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(method="lm", p0 =[1,1,1], maxfev=20000,)
        >>> model_name.statistician_RMSD(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_AIC(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_R2(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_R2a(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.summary(method="lm", p0 =[1,1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(method="lm", p0 =[1,1,1], maxfev=20000, apart = False,download_format="None")        
        """


        def __init__(self, url):
            self.url = url

        
        @property        
        def show(self):

            """Method to show the data organized in a table according to the chosen solubility model.
            """
            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)

            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            return DFF

        @property
        def temperature_values(self):

            """Method to show the values of the temperatures in a dataframe.
            """

            df = self.show
            tem = df["T"]
            return pd.DataFrame({"T":tem})
                    

        @property
        def mass_fractions(self):

            """Method to show the values of the mass fractions in a dataframe.
            """
            df = self.show
            mf = df.columns[1:]
            return pd.DataFrame({"w1":mf})

        @property
        def equation(self):
            
            """ Method to show the equation of the chosen solubility model.
            """
            salida = display(HTML('<h2> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Modified Apelblat Model Equation</h2>'))
            display(Math(r'$$\large{\ln(x_3) = A + \dfrac{B}{T} + C \cdot \ln T}$$'))
            return salida

    
        def __kernel(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False, opt = "calculate"):
            
            def fT(T,A,B,C):
                return np.exp(A + B/T + C*np.log(T))


            df = self.show
            W  = df.columns[1:].tolist()
            Temp = df["T"].values
            

            para_A,para_B,para_C = [],[],[]
            desv_A,desv_B,desv_C = [],[],[]
            desv_para_A,desv_para_B,desv_para_C = [],[],[]
            L_para,L_desv,L_desv_para= [para_A,para_B,para_C],[desv_A,desv_B,desv_C],[desv_para_A,desv_para_B,desv_para_C]
            
            for i in  W:
                xdat = df[i]
                Tdat = df["T"]
                popt, mcov= curve_fit(fT,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)
                
                for j in L_para:
                    j.append(popt[L_para.index(j)])
                    
                for k in L_desv:
                    k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))
                    
                for l in L_desv_para:
                    l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

        
            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]
        

            for i in W:

                wdat = len(Temp)*[i]
                Wdat = wdat

                tdat = Temp
                Tdat = tdat.tolist()

                x3_exp = df[i].values
                X3_exp =  x3_exp.tolist()

                x3_cal = fT(tdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)])
                X3_cal = x3_cal.tolist()

                RD = ((abs(x3_cal - x3_exp))/x3_exp).tolist()

                C_w    += Wdat
                C_temp += Tdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD
    
            arr_w   = np.array(C_w)
            arr_temp = np.array(C_temp)
            arr_exp = np.array(C_exp)
            arr_cal = np.array(C_cal)
            arr_RD  = np.array(C_RD )

            dataframe = pd.DataFrame({"w1":arr_w,'RD':arr_RD})

            MAPES = []

            for i in range(len(W)):

                df_mask = dataframe['w1'] == W[i]
                data_filter = dataframe[df_mask]
                MRDP = sum(data_filter["RD"])*100/len(data_filter["w1"])
                MAPES.append(MRDP)


            df_para      = pd.DataFrame({"w1":W,'A':para_A,'B':para_B,'C':para_C,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"w1":W,'A ± σ':desv_para_A,'B ± σ':desv_para_B,'C ± σ':desv_para_C,"MAPE":MAPES})
            df_cal       = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False, cg = True, cmap="Blues",download_format = "None"):
            
            """
            parameters
            ==========
            ### `parameters(method="lm",p0 =[1,1,1], maxfev=20000,sd = False, cg = True, cmap="Blues",download_format = "None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.

            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """
            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]

            D = self.__kernel(method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")

            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=5,formatter={"w1":"{:.2f}","MAPE":"{:.3f}"})                                                                                                   
            
            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="parameters_Modified Apelblat"


            extension = download_format
            namecols=["$w_1$","$A$","$B$","$C$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters=[f1,f2,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters=[f1,f2,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)            
                
            return DF
        

        def values(self,method="lm",p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None"):

            """
            values
            ======
            ### `values(method="lm", p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values and relative deviations
            in a dataframe. Download in different formats the values dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’).
            """

            DF = self.__kernel(method=method,p0=p0 , maxfev=maxfev, opt = "calculate")
            
            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_Modified Apelblat"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)            
            
            return DF

        def calculated_values(self,method="lm",p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None"):

            """
            calculated_values
            =================
            ###  `calculated_values(method="lm", p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            W = self.mass_fractions["w1"]
            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in self.temperature_values["T"]:
                df[i] = 10**(scale)* df[i]

            nombre ="calculated values_Modified Apelblat"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x


            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)

            return df


        def relative_deviations(self, method="lm",p0 =[1,1,1], maxfev=20000, cg = True, cmap="Blues",scale=0,download_format = "None"):

            """
            relative_deviations
            ===================
            ### `relative_deviations(method="lm",p0 =[1,1,1], maxfev=20000, cg = True, cmap="Blues",scale=0,download_format = "None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.relative_deviations(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            df = self.show
            Temp = df["T"].values
            
            W = self.mass_fractions["w1"]
            DF = self.__kernel( method=method,p0=p0 ,maxfev=maxfev, opt="calculate")


            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]

            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in self.temperature_values["T"]:
                d[i] = 10**(scale)* d[i]

            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=3,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="relative deviations_Modified Apelblat"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x
            def f2(x):return '%1.3f' % x

        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
            
            return df


        def statisticians(self,method="lm",p0 =[1,1,1], maxfev=20000,download_format = "None"):
            """
            statisticians
            =============
            ### `statisticians(method="lm", p0 =[1,1,1], maxfev=20000,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statisticians(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:           
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).             
             """            

            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD  = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 3  # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N    = len(DF["RD"])
            AIC  = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2   = 1 - (ss_res / ss_tot)
            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad = [MAPE,RMSD,AICc,R2,R2_a]
            names  = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="statisticians_Modified Apelblat"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)


            return df_estadis


        def statistician_MAPE(self,method="lm",p0 =[1,1,1], maxfev=20000):

            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error(MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:        
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            MAPE= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)

        def statistician_RMSD(self,method="lm",p0 =[1,1,1], maxfev=20000):
            """           
            statistician_RMSD
            =================
            ### `statistician_RMSD(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            RMSD= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,method="lm",p0 =[1,1,1], maxfev=20000):

            """           
            statistician_AIC
            =================
            ### `statistician_AIC(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            AIC= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,method="lm", p0 =[1,1,1],maxfev=20000):

            """           
            statistician_R2
            ===============
            ### `statistician_R2(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method t calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """           
 
            R2= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2 =",R2)
        
        def statistician_R2a(self,method="lm", p0 =[1,1,1],maxfev=20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            R2_a= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2 =",R2_a)


        def summary(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False,download_format="xlsx"):
            """
            summary
            =======
            ### `summary(method="lm",p0 =[1,1,1], maxfev=20000, sd = False,download_format="xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:               
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’). 
            """
           
            listaval     = self.values( method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values( method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations( method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters( method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians(method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval,calculados,diferencias,parametros,estadisticos], axis=1)

            extension = download_format

            nombre = "summary_Modified Apelblat"
            name_archi = URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3= nombre + name_archi +"."+extension
                    DATA.to_csv(url_3)            

            return DATA

        def plot(self,method="lm",p0 =[1,1,1], maxfev=20000,apart = False,download_format = "pdf"):

            """
            plot
            ====
            ### `plot(method="lm",p0 =[1,1,1], maxfev=20000,apart = False,download_format = "pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_apelblat(data)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### apart: bool, optional
            Separate the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’).
            """
            nombre= "plot_Modified Apelblat"

            df_values = self.values(method=method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]

            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +".tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+".tex"
            else:
                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +".tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+".tex"

            
            W = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]


            numerofilas = len(Temp)
            numerocolumnas = len(W)

            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name="w<sub>1</sub> = {w}".format(w=W[i]),
                                                text= Temp.tolist(),
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


                    fig.add_trace(go.Scatter(x=X,y=X,name="$x3^{Exp}=x3^{Cal}$",hoverinfo = "skip"))


                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="Modified Apelblat model",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)
                    grafica = fig.show()
                
                if extension == "tex":


                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("Modified Apelblat model",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)
                    grafica = plt.show()

                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi)

            if  apart == True:

                if extension != "tex":

                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =["w<sub>1</sub>"+" = "+str(i)+", "+"MAPE = "+str(RMDP[w.index(i)].round(1)) for i in w]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color="rgb(1,21,51)")),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(W)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title = "Modified Apelblat model",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF = self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =[r"$w_1$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[w.index(i)].round(1)) for i in w]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(W)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]
                        
                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)
                    grafica = plt.show()

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep")


            if apart == False:  
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)
                    
            if apart == True:
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"_sep."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)    
            return grafica

#CLASE PARA EL MODELO DE SOLUBILIDAD VAN’T HOFF

    class vant_hoff(dataset):

        """
        Van't Hoff Model
        ==========================
        ### `model.vant_hoff(dataset)`
        -------------------------------------------------------------------------------------------------
        Class of the van’t Hoff model, receives as argument a dataset 
        for find the model parameters, calculated values and make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.vant_hoff(data)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format="None")
        >>> model_name.values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(funtion = "fx",method="lm",p0 =[1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_RMSD(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2a(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.summary(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, separated = False,download_format="None")
        """
        def __init__(self,url):
            self.name = url

        
        @property
        def show(self):

            """Method to show the data organized in a table according to the chosen solubility model
            """
            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            
            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)

            return DFF

        @property
        def temperature_values(self):

            """Method to show the values of the temperatures in a dataframe.
            """
            df = self.show
            tem = df["T"]
            return pd.DataFrame({"T":tem})
                    

        @property
        def mass_fractions(self):

            """shows the values of the mass fraction in a dataframe.
            """

            df = self.show
            mf = df.columns[1:]
            return pd.DataFrame({"w1":mf})

        @property
        def equation(self):

            """ Method to show the equation of the chosen solubility model.
            """
            salida = display(HTML('<h2> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Van’t Hoff Model Equation</h2>'))
            display(Math(r'$$\large{\ln(x_3) = \dfrac{a}{T} + b }$$'))
            return salida

    
        def __kernel(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False, opt = "calculate"):

            def fT(T,a,b):
                return np.exp(a/T + b)  

            def fx(x,a,b):
                return a/(np.log(x)-b)


            df = self.show
            W  = df.columns[1:].tolist()
            Temp = df["T"].values
            

            para_a,para_b = [],[]
            desv_a,desv_b = [],[]
            desv_para_a,desv_para_b = [],[]
            L_para,L_desv,L_desv_para= [ para_a,para_b],[desv_a,desv_b],[desv_para_a,desv_para_b]
            
        
            if funtion== "fx":
                
                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fx,xdat,Tdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            if funtion == "fT":

                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fT,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]
        

            for i in W:

                wdat = len(Temp)*[i]
                Wdat = wdat

                tdat = Temp
                Tdat = tdat.tolist()

                x3_exp = df[i].values
                X3_exp =  x3_exp.tolist()

                x3_cal = fT(tdat,para_a[W.index(i)],para_b[W.index(i)])
                X3_cal = x3_cal.tolist()

                RD = (abs((x3_cal - x3_exp))/x3_exp).tolist()

                C_w    += Wdat
                C_temp += Tdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD
    
            arr_w    = np.array(C_w)
            arr_temp = np.array(C_temp)
            arr_exp  = np.array(C_exp)
            arr_cal  = np.array(C_cal)
            arr_RD   = np.array(C_RD )

            dataframe = pd.DataFrame({"w1":arr_w,'RD':arr_RD})

            MAPES = []

            for i in range(len(W)):

                df_mask = dataframe['w1'] == W[i]
                data_filter = dataframe[df_mask]
                MRDP = sum(data_filter["RD"])*100/len(data_filter["w1"])
                MAPES.append(MRDP)

            df_para = pd.DataFrame({"w1":W,'a':para_a,'b':para_b,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"w1":W,'a ± σ':desv_para_a,'b ± σ':desv_para_b,"MAPE":MAPES})
            df_cal  = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False, cg = True, cmap="Blues",download_format = "None"):

            """
            parameters
            ==========
            ### `parameters(funtion = "fx",method="lm",p0 =[1,1], maxfev=20000,sd = False, cg = True, cmap="Blues",download_format = "None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues"
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """
            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]

            D = self.__kernel(funtion = funtion, method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")
           
            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=5,formatter={"w1":"{:.2f}","MAPE":"{:.3f}"})


            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="parameters_Van't Hoff"


            extension = download_format
            namecols=["$w_1$","$a$","$b$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                                                                                                         
            return DF
        

        def values(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,scale=0,download_format="None"):

            """
            values
            ======
            ### `values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values and relative deviations
            in a dataframe. Download in different formats the values dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### funtion: {‘fx’, ‘fT’}, optional
            option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’).
            """

            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt = "calculate")

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_van't Hoff"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
            return DF


        def calculated_values(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,scale =0,download_format="None"):

            """
            calculated_values
            =================
            ###  `calculated_values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale =0,download_format="None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).        
            """
            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)
            
            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in self.temperature_values["T"]:
                df[i] = 10**(scale)* df[i]

            nombre ="calculated values_van't Hoff"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x

            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)            
            
            return df


        def relative_deviations(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,cg = True, cmap="Blues",scale=0,download_format = "None"):

            """
            relative_deviations
            ===================
            ### `relative_deviations(funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, cg = True, cmap="Blues",scale=0,download_format = "None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.relative_deviations(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).           
            """

            df = self.show
            Temp = df["T"].values

            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]
  
            
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in self.temperature_values["T"]:
                d[i] = 10**(scale)* d[i]

            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=3,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="relative deviations_ van't Hoff"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x
            def f2(x):return '%1.3f' % x

        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)

            return df        

        def statisticians(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,download_format="None"):

            """
            statisticians
            =============
            ### `statisticians(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,download_format="None)`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe.

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statisticians(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.            
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD  = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 2  # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N =len(DF["RD"])
            AIC = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2 = 1 - (ss_res / ss_tot)
            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad= [MAPE,RMSD,AICc,R2,R2_a]
            names = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="statisticians_van’t Hoff"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)

            return df_estadis

        def statistician_MAPE(self, funtion = "fx", method="lm",p0 =[1,1], maxfev=20000):

            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error(MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.   
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            MAPE= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)


        def statistician_RMSD(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000):
            """           
            statistician_RMSD
            =================
            ### `statistician_RMSD(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.    
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            RMSD= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000):
            """           
            statistician_AIC
            =================
            ### `statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            AIC= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,funtion = "fx",method="lm", p0 =[1,1],maxfev=20000):
            """           
            statistician_R2
            ===============
            ### `statistician_R2(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method t calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.     
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            R2= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2 =",R2)
        
        def statistician_R2a(self,funtion = "fx",method="lm", p0 =[1,1],maxfev=20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            R2_a= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2 =",R2_a)


        def summary(self, funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False,download_format = "xlsx"):

            """
            summary
            =======
            ### `summary(funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False,download_format = "xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.                 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of summary in the chosen format, excel format (‘xlsx’),
            comma separated values format (‘csv’). In the LaTex format the output can be copy/pasted 
            into a main LaTeX document, requires `\\usepackage{booktabs}`. Default is ‘xlsx’.
            """
            

            listaval     = self.values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval ,calculados,diferencias,parametros,estadisticos], axis=1)
            
            extension = download_format

            nombre = "summary_van't Hoff"
            name_archi = "-" + URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3= nombre + name_archi +"."+extension
                    DATA.to_csv(url_3)                

            return DATA

        def plot(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,apart = False,download_format = "pdf"):

            """
            plot
            ====
            ### `plot(funtion = "fx", method="lm",p0 =[1,1], maxfev=20000,apart = False,download_format = "pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff(data)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### apart: bool, optional
            Separates the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’).
            """

            nombre= "plot_van't Hoff"

            df_values = self.values(funtion =funtion, method= method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]
            
            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +".tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+".tex"
            else:
                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +".tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+".tex"

            
            W = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]


            numerofilas = len(Temp)
            numerocolumnas = len(W)

            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name="w<sub>1</sub> = {w}".format(w=W[i]),
                                                text= Temp.tolist(),
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


                    fig.add_trace(go.Scatter(x=X,y=X,name="$x3^{Exp}=x3^{Cal}$",hoverinfo = "skip"))


                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="van't Hoff equation",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)
                    grafica = fig.show()
                
                if extension == "tex":

                    
                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("van't Hoff equation",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)
                    grafica = plt.show()

                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi)

            if  apart == True:

                if extension != "tex":

                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =["w<sub>1</sub>"+" = "+str(i)+", "+"MAPE = "+str(RMDP[w.index(i)].round(1)) for i in w]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color='Red')),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(W)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title = "van't Hoff equation",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF = self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =[r"$w_1$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[w.index(i)].round(1)) for i in w]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(W)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]
                        
                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)

                    grafica = plt.show()

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep")


            if apart == False:  
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)
                    
            if apart == True:
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"_sep."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)    

            return grafica


#CLASE PARA EL MODELO DE SOLUBILIDAD VAN’T HOFF-YAWS

    class vant_hoff_yaws(dataset):

        """
        van't Hoff-Yaws Model
        ==========================
        ### `model.vant_hoff_yaws(dataset)`
        -------------------------------------------------------------------------------------------------
        Class of the Van't Hoff-Yaws model, receives as argument 
        a dataset to find the model parameters, calculated values and 
        make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.vant_hoff_yaws(data)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(method="lm", p0 =[1,1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format='None')
        >>> model_name.values(method="lm", p0 =[1,1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(method="lm", p0 =[1,1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(method="lm",p0 =[1,1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(method="lm", p0 =[1,1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_RMSD(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_AIC(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_R2(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.statistician_R2a(method="lm", p0 =[1,1,1], maxfev=20000)
        >>> model_name.summary(method="lm", p0 =[1,1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(method="lm", p0 =[1,1,1], maxfev=20000, apart = False,download_format="None")        
        """
        def __init__(self, url):
            self.url = url

        @property
        def show(self):
            
            """Method to show the data loaded as a dataframe.
            """

            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            
            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            return DFF

        @property
        def temperature_values(self):

            """Method to show the values of the temperatures in a dataframe.
            """
            df = self.show
            tem = df["T"]
            return pd.DataFrame({"T":tem})
                    

        @property
        def mass_fractions(self):

            """Method to show the values of the mass fractions in a dataframe.
            """
            df = self.show
            mf = df.columns[1:]
            return pd.DataFrame({"w1":mf})

        @property
        def equation(self):

            """ Method to show the equation of the chosen solubility model.
            """
            salida = display(HTML('<h2> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;van’t Hoff-Yaws Model Equation</h2>'))
            display(Math(r'$$\large{\ln(x_3) = a + \dfrac{b}{T}+\dfrac{c}{T^2}} $$'))
            return salida

    
        def __kernel(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False, opt = "calculate"):
            
            def fT(T,a,b,c):
                return np.exp(a+b/T+c/T**2)


            df = self.show
            W  = df.columns[1:].tolist()
            Temp = df["T"].values
            

            para_a,para_b,para_c = [],[],[]
            desv_a,desv_b,desv_c = [],[],[]
            desv_para_a,desv_para_b,desv_para_c = [],[],[]
            L_para,L_desv,L_desv_para= [para_a,para_b,para_c],[desv_a,desv_b,desv_c],[desv_para_a,desv_para_b,desv_para_c]
            
            for i in  W:
                xdat = df[i]
                Tdat = df["T"]
                popt, mcov= curve_fit(fT,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)
                
                for j in L_para:
                    j.append(popt[L_para.index(j)])
                    
                for k in L_desv:
                    k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))
                    
                for l in L_desv_para:
                    l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

        
            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]
        

            for i in W:

                wdat = len(Temp)*[i]
                Wdat = wdat

                tdat = Temp
                Tdat = tdat.tolist()

                x3_exp = df[i].values
                X3_exp =  x3_exp.tolist()

                x3_cal = fT(tdat,para_a[W.index(i)],para_b[W.index(i)],para_c[W.index(i)])
                X3_cal = x3_cal.tolist()

                RD = (abs((x3_cal - x3_exp))/x3_exp).tolist()

                C_w    += Wdat
                C_temp += Tdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD
    
            arr_w    = np.array(C_w)
            arr_temp = np.array(C_temp)
            arr_exp  = np.array(C_exp)
            arr_cal  = np.array(C_cal)
            arr_RD   = np.array(C_RD )

            dataframe = pd.DataFrame({"w1":arr_w,'RD':arr_RD})

            MAPES = []

            for i in range(len(W)):

                df_mask = dataframe['w1'] == W[i]
                data_filter = dataframe[df_mask]
                MRDP = sum(data_filter["RD"])*100/len(data_filter["w1"])
                MAPES.append(MRDP)

            df_para      = pd.DataFrame({"w1":W,'a':para_a,'b':para_b,'c':para_c,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"w1":W,'a ± σ':desv_para_a,'b ± σ':desv_para_b,'c ± σ':desv_para_c,"MAPE":MAPES})
            df_cal       = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False,cg = True, cmap="Blues",download_format = "None"):

            """
            parameters
            ==========
            ### `parameters(method="lm",p0 =[1,1,1], maxfev=20000,sd = False, cg = True, cmap="Blues",download_format = "None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.

            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues"
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]

            D = self.__kernel(method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")

            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=5,formatter={"w1":"{:.2f}","MAPE":"{:.3f}"})  

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="parameters_van’t Hoff-Yaws"


            extension = download_format
            namecols=["$w_1$","$a$","$b$","$c$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters=[f1,f2,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters=[f1,f2,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "ccccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)            

            return DF

        def values(self,method="lm",p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None"):

            """
            values
            ======
            ### `values(method="lm", p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values 
            and relative deviations in a dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’).
            """

            DF = self.__kernel(method=method,p0=p0 , maxfev=maxfev, opt = "calculate")

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_van’t Hoff-Yaws"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)            
            
            return DF
           

        def calculated_values(self,method="lm",p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None"):

            """
            calculated_values
            =================
            ###  `calculated_values(method="lm", p0 =[1,1,1], maxfev=20000,scale = 0,download_format = "None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            W = self.mass_fractions["w1"]
            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in self.temperature_values["T"]:
                df[i] = 10**(scale)* df[i]

            nombre ="calculated values_van’t Hoff-Yaws"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x


            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)

            return df

        def relative_deviations(self, method="lm",p0 =[1,1,1], maxfev=20000,cg = True, cmap="Blues",scale = 0, download_format = "None"):

            """
            relative_deviations
            ===================
            ### `relative_deviations(method="lm",p0 =[1,1,1], maxfev=20000, cg = True, cmap="Blues",scale = 0,download_format = "None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.relative_deviations(download_format = "tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            df = self.show
            Temp = df["T"].values
            
            W = self.mass_fractions["w1"]
            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            
            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]            
            
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in self.temperature_values["T"]:
                d[i] = 10**(scale)* d[i]
        
            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=3,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="relative deviations_van’t Hoff-Yaws"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.3f' % x
        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
            
            return df
              


        def statisticians(self,method="lm",p0 =[1,1,1], maxfev=20000,download_format = "None"):

            """
            statisticians
            =============
            ### `statisticians(method="lm", p0 =[1,1,1], maxfev=20000,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statisticians()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:           
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """            

            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD  = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 3  # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N =len(DF["RD"])
            AIC = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2 = 1 - (ss_res / ss_tot)
            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad= [MAPE,RMSD,AICc,R2,R2_a]
            names = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="statisticians_van't Hoff-Yaws"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)


            return df_estadis



        def statistician_MAPE(self,method="lm",p0 =[1,1,1], maxfev=20000):
            
            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error(MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:        
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            MAPE= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)

        def statistician_RMSD(self,method="lm",p0 =[1,1,1], maxfev=20000):
            
            """
            statistician_RMSD
            =================
            ### `statistician_RMSD(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            RMSD= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,method="lm",p0 =[1,1,1], maxfev=20000):

            """
            statistician_AIC
            =================
            ### `statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            AIC= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,method="lm", p0 =[1,1,1],maxfev=20000):
            """           
            statistician_R2
            ===============
            ### `statistician_R2(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """           
            R2= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2 =",R2)
        
        def statistician_R2a(self,method="lm", p0 =[1,1,1],maxfev=20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            R2_a= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2 =",R2_a)


        def summary(self, method="lm",p0 =[1,1,1], maxfev=20000, sd = False,download_format="xlsx"):

            """
            summary
            =======
            ### `summary(method="lm",p0 =[1,1,1], maxfev=20000, sd = False,download_format="xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:               
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’). In the LaTex format the 
            output can be copy/pasted into a main LaTeX document, requires `\\usepackage{booktabs}`.
            Default is ‘xlsx’.
            """
            
            listaval     = self.values( method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values( method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations( method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters( method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians(method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval ,calculados,diferencias,parametros,estadisticos], axis=1)

            extension = download_format

            nombre = "summary_van't Hoff-Yaws"
            name_archi = URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3= nombre + name_archi +"."+extension
                    DATA.to_csv(url_3)            

            return DATA
            

        def plot(self,method="lm",p0 =[1,1,1], maxfev=20000,apart = False,download_format = "pdf"):

            """
            plot
            ====
            ### `plot(method="lm",p0 =[1,1,1], maxfev=20000,separated = False,download_format = "pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.        

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### separated: bool, optional
            Separates the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’). 
            """
            nombre= "plot_van’t Hoff-Yaws"

            df_values = self.values(method=method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]

            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +".tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+".tex"
            else:
                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +".tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+".tex"

            
            W = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]


            numerofilas = len(Temp)
            numerocolumnas = len(W)
            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name="w<sub>1</sub> = {w}".format(w=W[i]),
                                                text= Temp.tolist(),
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


                    fig.add_trace(go.Scatter(x=X,y=X,name="$x3^{Exp}=x3^{Cal}$",hoverinfo = "skip"))


                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="van't Hoff-Yaws model",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)
                    grafica = fig.show()
                
                if extension == "tex":


                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("van't Hoff-Yaws model",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)
                    grafica = plt.show()

                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi)

            if  apart == True:

                if extension != "tex":

                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =["w<sub>1</sub>"+" = "+str(i)+", "+"MAPE = "+str(RMDP[w.index(i)].round(1)) for i in w]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color="rgb(1,21,51)")),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(W)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title = "van't Hoff-Yaws model",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF = self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =[r"$w_1$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[w.index(i)].round(1)) for i in w]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(W)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]
                        
                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)

                    grafica = plt.show()

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep")


            if apart == False:  
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)
                    
            if apart == True:
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"_sep."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)    
            return grafica

#CLASE PARA EL MODELO DE WILSON MODIFICADO

    class modified_wilson(dataset):

        """
        Modified Wilson Model
        ==========================
        ### `model.modified_wilson(dataset)`
        -------------------------------------------------------------------------------------------------
        Class of the modified Wilson model, receives as argument 
        a dataset to find the model parameters, calculated values and 
        make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.modified_wilson(data)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(method="lm", p0 =[1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format='None')
        >>> model_name.values(method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(method="lm",p0 =[1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(method="lm", p0 =[1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_RMSD(method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_AIC(method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2(method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2a(method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.summary(method="lm", p0 =[1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(method="lm", p0 =[1,1], maxfev=20000, apart = False,download_format="None")        
        """
        def __init__(self, url):
            self.url = url
        
        @property
        def show(self):

            """Method to show the data loaded as a dataframe.
            """

            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1)
                else:
                    DFF = df.rename({'w1': ''}, axis=1)
            
            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1)
                else:
                    DFF = df.rename({'w1': ''}, axis=1)

            return DFF


        @property
        def equation(self):
            """shows the equation model.
            """
            salida = display(HTML('<h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Modified Wilson Model Equation</h2>'))
            display(Math(r'$$\Large{\ln(x_3)=-1+\frac{w_1(1+\ln x_{3,1})}{w_1+(1-w_1)\lambda_{12}}+\frac{(1-w_1)(1+\ln x_{3,2})}{(1-w_1)+w_1 \lambda_{21}}}$$'))
            return salida

    
        def __kernel(self, method="lm",p0 =[1,1], maxfev=20000, sd = False, opt = "calculate"):

            df = self.show
            dff = df.drop([i for i in range(1,len(df["w1"])-1)],axis=0)
            W = df["w1"]

            Temp    = self.temperature_values["T"].values
            wdat    = df["w1"].values

            
            def fw(w1,λ12,λ21):
                return np.exp(-1+((w1+w1*np.log(x31))/(w1+(1-w1)*λ12))+(((1-w1)+(1-w1)*np.log(x32))/((1-w1)+w1*λ21)))


            para_λ12,para_λ21 = [],[]
            desv_para_λ12,desv_para_λ21 = [],[]

            L_para = [para_λ12,para_λ21]
            L_desv = [desv_para_λ12,desv_para_λ21]


            for i in Temp:
                x31       =  dff[i].values[1]
                x32       =  dff[i].values[0]
                x3_exp    =  df[i].values
                popt,mcov = curve_fit(fw,wdat,x3_exp,p0 =p0,method=method,maxfev=maxfev)

                for j in L_para:
                    j.append(popt[L_para.index(j)])

                for k in L_desv:
                    k.append(str(popt[L_desv.index(k)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv.index(k)]).round(3)))
            


            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]  

            for i in Temp:
        
                Tdat  =  len(df["w1"])*[float(i)]

                wdat  =  df["w1"].values
                Wdat  =   wdat.tolist()

                x31=  dff[i].values[1]
                x32=  dff[i].values[0]

    
                x3_exp =  df[i].values
                X3_exp =  x3_exp.tolist()


                x3_cal = fw(wdat,para_λ12[Temp.tolist().index(i)],para_λ21[Temp.tolist().index(i)])
                X3_cal = x3_cal.tolist()


                RD = (abs((x3_cal - x3_exp))/x3_exp).tolist()

                C_temp  += Tdat
                C_w    += Wdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD

            arr_w = np.array(C_w )
            arr_temp = np.array(C_temp)
            arr_exp = np.array(C_exp)
            arr_cal = np.array( C_cal)
            arr_RD  = np.array( C_RD )

            data_frame = pd.DataFrame({"w1":arr_w ,"T":arr_temp ,'RD':arr_RD})

            MAPES = []


            for i in range(len(Temp)):
                df_mask = data_frame['T'] == float(Temp[i])
                data_filter = data_frame[df_mask]
                MAPE = sum(data_filter["RD"])*100/len(data_filter["RD"])
                MAPES.append(MAPE)

            df_para = pd.DataFrame({"T":Temp,'λ12':para_λ12,'λ21':para_λ21,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"T":Temp,'λ12 ± σ':desv_para_λ12,'λ21 ± σ':desv_para_λ21,"MAPE":MAPES})
            df_cal  = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self,method="lm",p0 =[1,1], maxfev=20000, sd = False,cg = True, cmap="Blues",download_format = "None"):

            """
            parameters
            ==========
            ### `parameters(method="lm",p0 =[1,1], maxfev=20000,sd = False, cg = True, cmap="Blues",download_format = "None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.

            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues"
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]


            D = self.__kernel(method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")
            D['T'] = D['T'].astype(float)

            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                            .format(precision=5,formatter={"T":"{:.2f}","MAPE":"{:.3f}"}) 

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="parameters_Modified Wilson"


            extension = download_format
            namecols=["$w_1$","$\lambda_{12}$","$\lambda_{21}$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)            
                
            return DF                                                                                                    
     
    
        def values(self,method="lm",p0 =[1,1],maxfev=20000,scale = 0,download_format = "None"):

            """
            values
            ======
            ### `values(method="lm", p0 =[1,1], maxfev=20000,scale = 0,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values 
            and relative deviations in a dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’). 
            """


            DF = self.__kernel(method=method,p0=p0 , maxfev=maxfev, opt = "calculate")

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_Modified Wilson"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)            
            
            return DF           

        def calculated_values(self,method="lm",p0 =[1,1], maxfev=20000,scale = 0,download_format = "None"):

            """
            calculated_values
            =================
            ###  `calculated_values(method="lm", p0 =[1,1], maxfev=20000,scale = 0,download_format = "None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """


            W = self.mass_fractions["w1"]
            Temp    = self.temperature_values["T"].values.astype(float)

            DF = self.__kernel(method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in Temp:
                df[i] = 10**(scale)* df[i]

            nombre ="calculated values_Modified Wilson"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x


            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)

            return df


        def relative_deviations(self,method="lm",p0 =[1,1], maxfev=20000,cg = True, cmap="Blues",scale=0,download_format='None'):

            """
            relative_deviations
            ===================
            ### `relative_deviations(method="lm",p0 =[1,1], maxfev=20000, cg = True, cmap="Blues",scale=0,download_format = "None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.relative_deviations(download_format = "tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """
          
            W = self.mass_fractions["w1"]
            DF = self.__kernel(method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            Temp    = self.temperature_values["T"].values.astype(float)
            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]
  
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in Temp:
                d[i] = 10**(scale)* d[i]  

            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=4,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="relative deviations_Modified Wilson"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x
            def f2(x):return '%1.3f' % x

        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
            
            return df                  


        def statisticians(self,method="lm",p0 =[1,1], maxfev=20000,download_format = "None"):

            """
            statisticians
            =============
            ### `statisticians(method="lm", p0 =[1,1], maxfev=20000,download_format = "None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statisticians(download_format = "tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:           
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).  
            """            


            DF = self.__kernel( method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD  = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 2   # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N =len(DF["RD"])
            AIC = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2 = 1 - (ss_res / ss_tot)

            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad= [MAPE,RMSD,AICc,R2,R2_a]
            names = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="statisticians_Modified Wilson"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)

            return df_estadis



        def statistician_MAPE(self, method="lm",p0 =[1,1], maxfev=20000):

            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error(MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:        
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            MAPE= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)

        def statistician_RMSD(self,method="lm",p0 =[1,1], maxfev=20000):
            """
            statistician_RMSD
            =================
            ### `statistician_RMSD(method="lm", p0 =[1,1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            RMSD= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,method="lm",p0 =[1,1], maxfev=20000):

            """
            statistician_AIC
            =================
            ### `statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """


            AIC= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,method="lm", p0 =[1,1],maxfev=20000):
            """           
            statistician_R2
            ===============
            ### `statistician_R2(method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """           
            R2= self.statisticians(method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2 =",R2)
        
        def statistician_R2a(self,method="lm", p0 =[1,1],maxfev=20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(method="lm", p0 =[1,1], maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.modified_wilson(data)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            R2_a= self.statisticians( method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2 =",R2_a)


        def summary(self,method="lm",p0 =[1,1], maxfev=20000, sd = False,download_format="xlsx"):

            """
            summary
            =======
            ### `summary(method="lm",p0 =[1,1], maxfev=20000, sd = False,download_format="xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:               
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’). In the LaTex format the 
            output can be copy/pasted into a main LaTeX document, requires `\\usepackage{booktabs}`.
            Default is ‘xlsx’.
            """
        

            listaval     = self.values(method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values( method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations(method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters( method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians( method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval ,calculados,diferencias,parametros,estadisticos], axis=1)
            
            extension = download_format

            nombre = "summary_Modified Wilson"
            name_archi = URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3= nombre + name_archi +"."+extension
                    DATA.to_csv(url_3)            

            return DATA

        def plot(self,method="lm",p0 =[1,1], maxfev=20000,apart = False,download_format = "pdf"):
            """
            plot
            ====
            ### `plot(method="lm",p0 =[1,1], maxfev=20000,separated = False,download_format = "pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.        

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.vant_hoff_yaws(data)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### separated: bool, optional
            Separates the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’).
            """

            nombre=  "plot_Modified Wilson"

            df_values = self.values( method=method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]
            
            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +".tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+".tex"        
        
            else:

                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +".tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+".tex"


            W   = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]
            

            numerofilas    =  len(W)
            numerocolumnas =  len(Temp)
            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                    
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(Temp)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name= "T = {Tem}".format(Tem=Temp[i]),
                                                text= W.tolist(),
                                                hovertemplate= "x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>w<sub>1</sub>: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))

                    fig.add_trace(go.Scatter(x=X,y=X,name="$x3^{Exp}=x3^{Cal}$",hoverinfo = "skip"))

                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="Modified Wilson model",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)            

                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)
                    grafica =fig.show()

                if extension == "tex":

                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(Temp)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("Modified Wilson model",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)
                    grafica = plt.show()  

                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi)

            if  apart == True:
                
                if extension != "tex":

                    cols = 2
                    rows = ceil(len(Temp)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    t= Temp.values.tolist()
                    name =["T"+" = "+str(i)+", "+"MAPE = "+str(RMDP[t.index(i)].round(1)) for i in t]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(Temp)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(Temp)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color="rgb(1,21,51)")),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(Temp)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(Temp)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title = "Modified Wilson model",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(Temp)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF = self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    t= Temp.values.tolist()
                    name =[r"$T$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[t.index(i)].round(1)) for i in t]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(Temp)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]
                        
                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)

                    grafica = plt.show()

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep")


            if apart == False:  
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)
                    
            if apart == True:
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"_sep."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)    
            return grafica


#CLASE PARA EL MODELO DE SOLUBILIDAD BUCHOWSKI KSIAZCZAK
    class buchowski_ksiazaczak(dataset):

        """
        Buchowski Ksiazaczak Model
        ==========================
        ### `model.buchowski_ksiazaczak(dataset,Tf)`
        -------------------------------------------------------------------------------------------------
        Class of the Buchowski Ksiazaczak model, receives as argument 
        a dataset and the melting temperature Tf for find the model parameters, 
        calculated values and make the plotting graphs.
        --------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name = model.buchowski_ksiazaczak(data,Tf)

        ---------------------------------------------------------------------------------------------------
        ## Methods
        The methods with their default parameters that can be applied to this model
        are the following:
        >>> model_name.show
        >>> model_name.equation
        >>> model_name.mass_fractions
        >>> model_name.temperature_values
        >>> model_name.experimental_values(scale=0, download_format='None')
        >>> model_name.parameters(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False, gc = True, cmap="Blues",download_format="None")
        >>> model_name.values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.calculated_values(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,scale=0,download_format="None")
        >>> model_name.relative_deviations(funtion = "fx",method="lm",p0 =[1,1], maxfev=20000, gc = True, cmap="Blues",scale=0,download_format="None")
        >>> model_name.statisticians(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000,download_format="None")
        >>> model_name.statisticians_MAPE(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_RMSD(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_AIC(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.statistician_R2a(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000)
        >>> model_name.summary(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, sd = False,download_format="None")
        >>> model_name.plot(funtion = "fx",method="lm", p0 =[1,1], maxfev=20000, apart = False,download_format="None")
        """

        def __init__(self,url,Tf):
            self.name = url
            self.Tf = Tf
        
        @property
        def show(self):

            """Method to show the data organized in a table according to the chosen solubility model.
            """
            
            L = URL.split(".")

            if L[-1]=="csv":
                df = pd.read_csv(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
            
            if L[-1]=="xlsx":
                df = pd.read_excel(URL)
                if "x1" in df.columns or "x2" in df.columns:
                    DFF = df.drop(['x1',"x2"], axis=1).rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)
                else:
                    DFF = df.rename({'w1': ''}, axis=1).set_index('').transpose().reset_index().rename({'index': 'T'}, axis=1).astype(float)

            return DFF

        @property
        def temperature_values(self):

            """Method to show the values of the temperatures in a dataframe.
            """

            df = self.show
            tem = df["T"]
            return pd.DataFrame({"T":tem})
                    

        @property
        def mass_fractions(self):

            """Method to show the values of the mass fractions in a dataframe.
            """

            df = self.show
            mf = df.columns[1:]
            return pd.DataFrame({"w1":mf})

        @property
        def equation(self):
            """ Method to show the equation of the chosen solubility model.
            """
            salida = display(HTML('<h2>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Buchowski-Ksiazczak Model Equation</h2>'))
            display(Math(r'$$\large{\ln \left[ 1+ \dfrac{\lambda (1 -x_3)}{x_3} \right] = \lambda h \left( \dfrac{1}{T} - \dfrac{1}{T_f}  \right)}$$'))
            return salida

    
        def __kernel(self,funtion = "fx", method="lm",p0 =[1,1], maxfev=20000, sd = False, opt = "calculate"):

            Tf = self.Tf

            def fx(x,λ,h):
                return 1/((np.log(1+(λ*(1-x)/x))/(λ*h))+1/Tf)

            def fT1(T,λ,h):
                return (λ*np.exp(λ*h/Tf))/(λ*np.exp(λ*h/Tf)-np.exp(λ*h/Tf)+np.exp(λ*h/T))


            def fT2(T,λ,h):
                return (λ*np.exp(h*λ*(T-Tf)/(Tf*T)))/(((λ-1)*np.exp(h*λ*(T-Tf)/(Tf*T)))+1)


            df = self.show
            W  = df.columns[1:].tolist()
            Temp = df["T"].values
            

            para_λ,para_h = [],[]
            desv_λ,desv_h = [],[]
            desv_para_λ,desv_para_h = [],[]
            L_para,L_desv,L_desv_para= [para_λ,para_h],[desv_λ,desv_h],[desv_para_λ,desv_para_h]
            
        
            if funtion== "fx":
                
                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fx,xdat,Tdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            if funtion == "fT1":

                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fT1,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            if funtion == "fT2":

                for i in  W:
                    xdat = df[i]
                    Tdat = df["T"]
                    popt, mcov= curve_fit(fT2,Tdat,xdat,method= "lm",p0=p0,maxfev=20000)

                    for j in L_para:
                        j.append(popt[L_para.index(j)])

                    for k in L_desv:
                        k.append(np.sqrt((np.diag(mcov))[L_desv.index(k)]))

                    for l in L_desv_para:
                        l.append(str(popt[L_desv_para.index(l)].round(3)) + " ± " + str(np.sqrt((np.diag(mcov))[L_desv_para.index(l)]).round(3)))

            
            C_w, C_temp, C_exp, C_cal, C_RD  = [],[],[],[],[]
        

            for i in W:

                wdat = len(Temp)*[i]
                Wdat = wdat

                tdat = Temp
                Tdat = tdat.tolist()

                x3_exp = df[i].values
                X3_exp =  x3_exp.tolist()

                x3_cal = fT2(tdat,para_λ[W.index(i)],para_h[W.index(i)])
                X3_cal = x3_cal.tolist()

                RD = (abs((x3_cal - x3_exp))/x3_exp).tolist()

                C_w    += Wdat
                C_temp += Tdat
                C_exp  += X3_exp
                C_cal  += X3_cal
                C_RD   += RD
    
            arr_w   = np.array(C_w)
            arr_temp = np.array(C_temp)
            arr_exp = np.array(C_exp)
            arr_cal = np.array(C_cal)
            arr_RD  = np.array(C_RD )

            dataframe = pd.DataFrame({"w1":arr_w,'RD':arr_RD})

            MAPES = []

            for i in range(len(W)):

                df_mask = dataframe['w1'] == W[i]
                data_filter = dataframe[df_mask]
                MRDP = sum(data_filter["RD"])*100/len(data_filter["w1"])
                MAPES.append(MRDP)

            df_para = pd.DataFrame({"w1":W,'λ':para_λ,'h':para_h,"MAPE":MAPES})
            df_para_desv = pd.DataFrame({"w1":W,'λ ± σ':desv_para_λ,'h ± σ':desv_para_h,"MAPE":MAPES})
            df_cal  = pd.DataFrame({"w1":arr_w,'T': arr_temp,"x3_Exp":arr_exp,"x3_Cal":arr_cal, "RD":arr_RD })

            if opt == "calculate" and sd == False:
                df_kernel = df_cal
            if opt == "parameters" and sd == True:
                df_kernel = df_para_desv
            if opt == "parameters" and sd == False:
                df_kernel = df_para
            return  df_kernel 

        def parameters(self,funtion = "fx",method = "lm",p0 = [1,1], maxfev = 20000,sd = False,cg = True,cmap = "Blues",download_format = "None"):

            """
            parameters
            ==========
            ### `parameters(funtion="fx",method="lm",p0=[1,1],maxfev=20000,sd=False,cg=True,cmap="Blues",download_format="None")`
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            Method to show the model fit parameters with their standard deviation for each mass fraction 
            in a dataframe. Download in different formats the parameters dataframe.
            --------------------------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.parameters(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            Shows the standard deviations for each parameter. Default is False.
            - ### cg: bool, optional
            Shows a color gradient for the "MAPE" column to identify high and low error values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of parameters in the chosen format,
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’).
            """

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx["MAPE"]]

            D = self.__kernel(funtion = funtion, method=method,p0 =p0,maxfev=maxfev, sd = sd, opt = "parameters")
           
            if cg == False:
                DF = D
            if cg == True:
                DF=  D.style.background_gradient(cmap=cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=5,formatter={"w1":"{:.2f}","MAPE":"{:.3f}"})


            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="parameters_Buchowski Ksiazczak"


            extension = download_format
            namecols=["$w_1$","$\lambda$","$h$","$RMD\%$"]
     

            def f1(x): return '%1.2f' % x

            def f2(x):return '%1.3f' % x

            def f3(x):return '%1.2f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre +"-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    if sd == False:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters=[f1,f2,f2,f3],header=namecols,escape =False)
                    if sd == True:
                        D.to_latex(url_8,index=False,column_format= "cccc", formatters={"w1":f1,"MAPE":f3},header=namecols,escape =False)

                environment_table(url_8)
                generate_pdf(nombre + "-"+ name_archi)


            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_excel(url_8,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_8 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)
                    files.download(url_8)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    D.to_csv(url_8)

            return DF
        

        def values(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,scale = 0,download_format = "None"):

            """
            values
            ======
            ### `values(funtion="fx",method="lm",p0=[1,1],maxfev=20000,scale=0,download_format="None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the calculated values, experimental values and relative deviations
            in a dataframe. Download in different formats the values dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.values(scale=0,download_format="xlsx")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below:

            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of experimental values and calculated values
            in the chosen format, excel format (‘xlsx’), comma separated values format (‘csv’),
            LaTeX format (‘tex’). 
            """
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt = "calculate")

            name_archi = URL.split("/")[-1].split(".")[-2]
            nombre ="values_Buchowski Ksiazczak"

            DF["x3_Exp"] = 10**(scale)*DF["x3_Exp"]
            DF["x3_Cal"] = 10**(scale)*DF["x3_Cal"]

            extension = download_format
            namecols=["$w_1$","$T$","$x_3^{Exp}$","$x_3^{Cal}$","$RD$"]
     

            def f1(x): return '%.2f' % x

            def f2(x): return '%.4f' % x

            def f3(x): return '%.3f' % x

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)
                    files.download(url_12)
                else:
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_latex(url_12,index=False,column_format= "ccccc", formatters=[f1,f1,f2,f2,f3],header=namecols,escape =False)

                environment_table(url_12)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)
                    files.download(url_12)
                else:
                    url_12 = nombre + "-"+ name_archi +"."+extension
                    DF.to_excel(url_12,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_12 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)
                    files.download(url_12)
                else:
                    url_8 = nombre + "-"+ name_archi +"."+extension
                    DF.to_csv(url_12)

            return DF


        def calculated_values(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,scale = 0,download_format = "None"):

            """
            calculated_values
            =================
            ###  `calculated_values(funtion="fx",method="lm",p0=[1,1],maxfev=20000,scale=0,download_format="None")`
            -----------------------------------------------------------------------------------------------------------------------------------------
            Method to show the table of calculated values of the solubility according to temperatures 
            and mass fractions in a dataframe. Download in different formats the calculated values dataframe.

            ---------------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.calculated_values(scale =3,download_format="tex")  

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 

            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations.Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All calculated mole fractions are
            multiplied by this power .e.g. scale = 3 multiply the mole fractions by the
            power 10^3. Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of calculated values in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","RD"],axis=1).rename({'T':'','x3_Cal':i}, axis=1).set_index('').transpose()
                L.append(line)

            df = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = df.columns[1:].astype(str).tolist()

            for i in self.temperature_values["T"]:
                df[i] = 10**(scale)* df[i]

            nombre ="calculated values_Buchowski Ksiazczak"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x

            if scale != 0:
                def f2(x):return '%1.2f' % x
            else:
                def f2(x):return '%1.5f' % x


            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_latex(url_9,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_9)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_excel(url_9,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_9 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
                    files.download(url_9)
                else:
                    url_9 = nombre + "-"+ name_archi +"."+extension
                    df.to_csv(url_9)
            return df


        def relative_deviations(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,cg = True,cmap = "Blues",scale = 0,download_format = "None"):

            """
            relative_deviations
            ===================
            ### `relative_deviations(funtion="fx",method="lm",p0=[1,1],maxfev=20000,cg=True,cmap="Blues",scale = 0,download_format="None")`
            ----------------------------------------------------------------------------------------------------------------------------
            Method to show the table relative deviations for each value calculated according
            to temperatures and mass fractions in a dataframe. Download in different formats 
            the relative deviations dataframe.
            
            ----------------------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.relative_deviations(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 

            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### cg: bool, optional
            Shows a color gradient to all columns for identify high and low deviations values.
            Default is True.
            - ### cmap: str or colormap
            Change the color of the color gradient according to matplotlib colormap.
            Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
            https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
            - ### scale: int, optional
            Option to indicate the exponent of the power of 10. All relative deviations are
            multiplied by this power .e.g. scale = 2 multiply the relative deviations by the
            power 10^2 (relative percentage deviations). Default is scale=0.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of relative deviations in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """


            df = self.show
            Temp = df["T"].values
            
            W = self.mass_fractions["w1"]
            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            idx = pd.IndexSlice
            slice_1 = idx[idx[:], idx[Temp[0]:Temp[-1]]]
           
            L = []
            for i in W: 
                mask = DF['w1'] == i
                data_filter = DF[mask]
                line = data_filter.drop(["w1","x3_Exp","x3_Cal"],axis=1).rename({'T':'','RD':i}, axis=1).set_index('').transpose()
                L.append(line)

            d = pd.concat(L,axis =0).reset_index().rename({'index': 'w1'}, axis=1).rename({'T': ''},axis=1)

            for i in self.temperature_values["T"]:
                d[i] = 10**(scale)* d[i]

            if cg == False:
                df = d
            if cg == True:
                df =d.style.background_gradient(cmap= cmap ,subset=slice_1,low=0, high=0.6)\
                           .format(precision=3,formatter={"w1":"{:.2f}"})

            name_archi = URL.split("/")[-1].split(".")[-2]

            cols = d.columns[1:].astype(str).tolist()

            nombre ="relative deviations_Buchowski Ksiazczak"
        
            extension = download_format
            namecols=["$w_1$"]+["$"+i+"$" for i in cols]

            def f1(x):return '%1.2f' % x
            def f2(x):return '%1.3f' % x

        
            if extension == "tex":     
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_latex(url_10,index=False,column_format= (len(cols)+1)*"c", formatters=[f1]+(len(cols))*[f2],header=namecols,escape =False)

                environment_table(url_10)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_excel(url_10,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_10 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
                    files.download(url_10)
                else:
                    url_10 = nombre + "-"+ name_archi +"."+extension
                    d.to_csv(url_10)
            return df

        def statisticians(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000,download_format = "None"):

            """
            statisticians
            =============
            ### `statisticians(funtion="fx",method="lm",p0=[1,1],maxfev=20000,download_format="None")`
            -------------------------------------------------------------------------------------------------------------------
            Method to show the table of statisticians of the model in a dataframe.

            -Mean Absolute Percentage Error (MAPE).
            -Root Mean Square Deviation (RMSD).
            -Akaike Information Criterion corrected (AICc).
            -Coefficient of Determination (R^2).
            -Adjusted Coefficient of Determination (R^2_a).

            Download in different formats the statisticians dataframe.

            ------------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statisticians(download_format="tex")

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.            
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
            Option to download the dataframe of statisticians in the chosen format, 
            excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
            """

            DF = self.__kernel(funtion = funtion, method=method,p0=p0 , maxfev=maxfev, opt="calculate")

            MAPE = sum(abs(DF["RD"]))*100/len(DF["RD"])
            MRD = sum(DF["RD"])/len(DF["RD"])
            MRDP = sum(DF["RD"])*100/len(DF["RD"])

            ss_res = np.sum((DF["x3_Cal"] - DF["x3_Exp"])**2)
            ss_tot = np.sum((DF["x3_Exp"] - np.mean(DF["x3_Exp"]))**2)

            RMSD = np.sqrt(ss_res/len(DF["x3_Exp"]))

            k = 2  # Número de parámetros del modelo
            Q = 1   # Número de variables independientes
            N =len(DF["RD"])
            AIC = N*np.log(ss_res/N)+2*k
            AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

            R2 = 1 - (ss_res / ss_tot)
            R2_a = 1-((N-1)/(N-Q-1))*(1- R2**2)

            L_stad= [MAPE,RMSD,AICc,R2,R2_a]
            names = ["MAPE","RMSD","AICc","R2","R2_a"]
            names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

            df_estadis = pd.DataFrame({"statisticians":names,"values":L_stad})
            df_est= pd.DataFrame({"statisticians":names_tex,"values":L_stad})

            cols = df_estadis.columns
            name_archi = URL.split("/")[-1].split(".")[-2]
            
            nombre ="statisticians_Buchowski Ksiazczak"
            extension = download_format
            

            if extension == "tex":
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_est.to_latex(url_11,index=False,column_format= len(cols)*"c",escape =False)
                    files.download(url_11)

                environment_table(url_11)
                generate_pdf(nombre + "-"+ name_archi)

            if extension == "xlsx":  
                if entorno == "/usr/bin/python3" :
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_excel(url_11,sheet_name=nombre)

            if extension == "csv":   
                if entorno == "/usr/bin/python3":
                    url_11 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)
                    files.download(url_11)
                else:
                    url_11 = nombre + "-"+ name_archi +"."+extension
                    df_estadis.to_csv(url_11)

            return df_estadis

        def statistician_MAPE(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000):

            """
            statistician_MAPE
            =================
            ### `statistician_MAPE(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Mean Absolute Percentage Error (MAPE).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_MAPE()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.   
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            MAPE= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][0]
            return print("Mean Absolute Percentage Error, MAPE = ",MAPE)

        def statistician_RMSD(self,funtion = "fx",method = "lm",p0 = [1,1], maxfev = 20000):

            """           
            statistician_RMSD
            =================
            ### `statistician_RMSD(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Root Mean Square Deviation(RMSD).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_RMSD()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.    
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            RMSD= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][1]
            return print("Root Mean Square Deviation, RMSD = ",RMSD)
            
        def statistician_AIC(self,funtion = "fx", method ="lm",p0 = [1,1], maxfev = 20000):

            """           
            statistician_AIC
            =================
            ### `statistician_AIC(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Akaike Information Criterion corrected(AICc).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_AIC()

            -------------------------------------------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.      
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """

            AIC= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][2]
            return print("Akaike Information Criterion corrected , AICc = ",AIC)

        def statistician_R2(self,funtion = "fx",method = "lm",p0 = [1,1],maxfev = 20000):

            """           
            statistician_R2
            ===============
            ### `statistician_R2(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Coefficient of Determination(R2).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_R2()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.     
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            R2= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][3]
            return print("Coefficient of Determination, R2a =",R2)
        
        def statistician_R2a(self,funtion = "fx",method = "lm", p0 = [1,1],maxfev = 20000):

            """           
            statistician_R2a
            =================
            ### `statistician_R2a(funtion="fx",method="lm",p0=[1,1],maxfev=20000)`
            -----------------------------------------------------------------------------------------------------------------
            Method to calculate the Adjusted Coefficient of Determination(R2a).
            
            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.statistician_R2a()

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.       
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
             """
            R2_a= self.statisticians(funtion = funtion, method=method,p0 =p0, maxfev=maxfev)["values"][4]
            return print("Adjusted Coefficient of Determination, R2a =",R2_a)


        def summary(self,funtion = "fx", method = "lm",p0 = [1,1], maxfev = 20000, sd = False,download_format = "xlsx"):

            """
            summary
            =======
            ### `summary(funtion="fx",method="lm",p0=[1,1],maxfev=20000,sd=False,download_format="xlsx")`
            ---------------------------------------------------------------------------------------------------------------
            Method to show a summary with calculated values, relative deviations, parameters and statistician
            of the model in a dataframe. Download in different formats the summary dataframe.

            -----------------------------------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.summary()
            
            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            the calculations. Default is ‘fx’.                 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### sd: bool, optional
            shows the standard deviations for each of the parameters. Default is False.
            - ### download_format: {‘xlsx’, ‘csv’}, optional
            Option to download the dataframe of summary in the chosen format, excel format (‘xlsx’),
            comma separated values format (‘csv’). In the LaTex format the output can be copy/pasted 
            into a main LaTeX document, requires `\\usepackage{booktabs}`. Default is ‘xlsx’.
            """
            

            listaval     = self.values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            calculados   = self.calculated_values(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)
            diferencias  = self.relative_deviations(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,cg = False) 
            parametros   = self.parameters(funtion = funtion, method = method,p0 =p0, maxfev=maxfev,sd = sd,cg = False)
            estadisticos = self.statisticians(funtion = funtion, method = method,p0 =p0, maxfev=maxfev)

            DATA = pd.concat([listaval,calculados,diferencias,parametros,estadisticos], axis=1)
            
            extension = download_format

            nombre = "summary_Buchowski Ksiazczak"
            name_archi = "-" + URL.split("/")[-1].split(".")[-2]

            if extension == "xlsx":
                if entorno == "/usr/bin/python3":
                    url_1= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
                    files.download(url_1)
                else:
                    url_1= nombre + name_archi +"."+extension
                    DATA.to_excel(url_1,sheet_name=name_archi)
            
            if extension == "csv":
                if entorno == "/usr/bin/python3":
                    url_3= "/content/"+ nombre + "-"+ name_archi +"."+extension
                    DATA.to_csv(url_3)
                    files.download(url_3)
                else:
                    url_3= nombre + name_archi +"."+extension
                    DATA.to_csv(url_3)            
            
            return DATA


        def plot(self,funtion = "fx", method ="lm",p0 = [1,1], maxfev = 20000,apart = False,download_format = "pdf"):
            """
            plot
            ====
            ### `plot(funtion="fx",method="lm",p0 =[1,1],maxfev=20000,apart = False,download_format="pdf")`
            ----------------------------------------------------------------------------------------
            Method to shows the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions. Download in different formats 
            the graph.

            -----------------------------------------------------------------------------------------
            # Examples
            >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
            >>> model_name = model.buchowski_ksiazaczak(data,Tf)
            >>> model_name.plot()
            >>> model_name.plot(separated = True) #separated according to mass fractions

            ------------------------------------------------------------------------------------------------------------------
            ## Parameters 
            The explanation of the parameters of this method are presented below: 
            - ### funtion: {‘fx’, ‘fT1’,‘fT2’}, optional
            Option to choose the function in terms of solubilities or temperatures for execution 
            - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
            Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
            for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
            work when the number of observations is less than the number of variables, use ‘trf’
            or ‘dogbox’ in this case.
            - ### p0: array_like, optional
            Initial guess for the parameters (length N). If None, then the initial values will 
            all be 1 (if the number of parameters for the function can be determined using 
            introspection, otherwise a ValueError is raised).
            - ### maxfev: int, optional
            The maximum number of calls to the function. Default is 20000.
            - ### separated: bool, optional
            Separates the graph according to mass fractions.
            - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
            Option to download the graph of calculated values and experimental values of solubility
            completely or separately according to mass fractions, pdf format (‘pdf’), png format (‘png’),
            LaTeX format (‘tex’).
            """

            nombre= "plot_Buchowski Ksiazczak"

            df_values = self.values(funtion =funtion, method= method,p0 =p0, maxfev=maxfev)

            name_archi ="-" + URL.split("/")[-1].split(".")[-2]
            
            if entorno == "/usr/bin/python3":
                url_2 = "/content/"+ nombre +  name_archi +".pdf"
                url_4 = "/content/"+ nombre +  name_archi +".png"
                url_12 = "/content/"+ nombre +  name_archi +".tex"
                url_5 = "/content/"+ nombre +  name_archi +"_sep"+".pdf"
                url_6 = "/content/"+ nombre +  name_archi +"_sep"+".png"
                url_13 = "/content/"+ nombre +  name_archi +"_sep"+".tex"
            else:
                url_2 = nombre +  name_archi +".pdf"
                url_4 = nombre +  name_archi +".png"
                url_12 = nombre +  name_archi +".tex"
                url_5 = nombre +  name_archi +"_sep"+".pdf"
                url_6 = nombre +  name_archi +"_sep"+".png"
                url_13 = nombre +  name_archi +"_sep"+".tex"

            
            W = self.mass_fractions["w1"]
            Temp = self.temperature_values["T"]


            numerofilas = len(Temp)
            numerocolumnas = len(W)

            L = [numerofilas*i for i in range(numerocolumnas+2)]

            extension= download_format

            if apart == False :
                
                if extension != "tex":
                
                    fig = go.Figure()
                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                name="w<sub>1</sub> = {w}".format(w=W[i]),
                                                text= Temp.tolist(),
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


                    fig.add_trace(go.Scatter(x=X,y=X,name="$x3^{Exp}=x3^{Cal}$",hoverinfo = "skip"))


                    fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")
                    fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
                    fig.update_layout(title="Buchowski-Ksiazczak λh model",showlegend=True,title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
                    #fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
                    fig.write_image(url_2)
                    fig.write_image(url_4)
                    grafica = fig.show()
                
                if extension == "tex":

                    plt.rcParams["figure.figsize"] = (10, 8)
                    fig, ax = plt.subplots()

                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X"]

                    X = np.linspace(min(df_values["x3_Exp"]),max(df_values["x3_Exp"]),200)

                    for i in range(len(W)):
                        plt.scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]], c = "k",marker=marker[i])

                    x = [min(df_values["x3_Exp"]),max(df_values["x3_Exp"])]
                    y = [min(df_values["x3_Cal"]),max(df_values["x3_Cal"])]

                    ax.plot(x,y,color='black',markersize=0.1)
                    ax.set_title("Buchowski-Ksiazczak "+ r"$\lambda h$" + " model",fontsize='large')


                    ax.xaxis.set_ticks_position('both')
                    ax.yaxis.set_ticks_position('both')
                    ax.tick_params(direction='in')


                    ax.set_xlabel("$x_{3}^{exp}$")
                    ax.set_ylabel("$x_{3}^{cal}$")
                    
                    tikzplotlib.save(url_12)
                    grafica = plt.show()

                    environment_graph(url_12)
                    generate_pdf(nombre +  name_archi)


            if  apart == True:

                if extension != "tex":

                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(1,rows+1):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(1,cols+1))

                    DF = self.__kernel(method=method,p0 =p0,maxfev=maxfev, opt = "parameters")

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =["w<sub>1</sub>"+" = "+str(i)+", "+"MAPE = "+str(RMDP[w.index(i)].round(1)) for i in w]

                    fig = make_subplots(rows=rows, cols=cols,subplot_titles=name)

        
                    for i in range(len(W)):
                        fig.add_trace(go.Scatter(x=df_values["x3_Exp"][L[i]:L[i+1]], y=df_values["x3_Cal"][L[i]:L[i+1]],
                                                text= Temp.tolist(),
                                                name = "",
                                                hovertemplate="x<sub>3</sub><sup>Exp</sup>: %{x}<br>x<sub>3</sub><sup>Cal</sup>: %{y}<br>T: %{text}<br>",
                                                mode='markers',
                                                showlegend= False,
                                                marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        X = np.linspace(min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]]),200)
                        fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color='Red')),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

                    for i in range(len(W)):
                        fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

                    for i in range(len(W)):
                        fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")

                    fig.update_layout(title ="Buchowski-Ksiazczak λh model",height=100*len(W)+300, width= 1300,showlegend=False)

                    fig.write_image(url_5,height=100*len(W)+300, width= 1300)
                    fig.write_image(url_6,height=100*len(W)+300, width= 1300)

                    grafica = fig.show()

                if extension == "tex":
                    
                    cols = 2
                    rows = ceil(len(W)/cols)

                    L_r = []
                    for i in range(0,rows):
                        L_r += cols*[i]

                    L_row =40*L_r
                    L_col =40*list(range(0,cols))


                    DF =self.parameters(cg = False)

                    RMDP = DF["MAPE"].values

                    w= W.values.tolist()
                    name =[r"$w_1$"+" = "+str(i)+", "+"$MAPE = $"+str(RMDP[w.index(i)].round(1)) for i in w]


                    marker = 10*['X','H',"+",".","o","v","^","<",">","s","p","P","*","h","X","D"]

                    plt.rcParams["figure.figsize"] = (30, 50)

                    fig, axs = plt.subplots(rows, cols)

                    for i in range(len(W)):
                        x=df_values["x3_Exp"][L[i]:L[i+1]]
                        y=df_values["x3_Cal"][L[i]:L[i+1]]

                        axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker=marker[i])
                        axs[L_row[i], L_col[i]].set_title(name[i],fontsize='large')
                        axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                        axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                        axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                        axs[L_row[i], L_col[i]].tick_params(direction='in')

                        X = [min(df_values["x3_Exp"][L[i]:L[i+1]]),max(df_values["x3_Exp"][L[i]:L[i+1]])]
                        Y = [min(df_values["x3_Cal"][L[i]:L[i+1]]),max(df_values["x3_Cal"][L[i]:L[i+1]])]
                        axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

                    fig.subplots_adjust(hspace=0.5)


                    tikzplotlib.save(url_13)
                    grafica = plt.show()

                    environment_graph_apart(url_13,cols,rows)
                    generate_pdf(nombre + name_archi+"_sep")


            if apart == False:  
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)
                    
            if apart == True:
                if entorno == "/usr/bin/python3":
                    url= "/content/"+nombre + name_archi +"_sep."+extension
                    files.download(url)
                else:
                    url= nombre + name_archi +"."+extension
                    print(url)    

            return grafica

        #modified_apelblat   
        #vant_hoff           
        #vant_hoff_yaws       
        #modified_wilson      
        #buchowski_ksiazaczak 
        #NRTL                 
        #wilson               
        #weibull             

class models(model.modified_apelblat,model.vant_hoff,model.vant_hoff_yaws,model.modified_wilson,model.buchowski_ksiazaczak):

    """class to print summary statistics of all models and summary plots 
    for the dataset according to Tf and ΔHf.
    # models summary 
    ----------------
    `statistics(dataset,Tf,ΔHf)`
    `plots(dataset,Tf,ΔHf)`
    """
    
    def __init__(self):
        
        self.statisticians = self.statisticians()
        self.plots      = self.plots()
 
    

    def statisticians(self,Tf = " ",ΔHf= " ",method="lm",p0_ma =[1,1,1],p0_vh =[1,1],p0_vhy =[1,1,1],p0_mw =[1,1],p0_bk=[1,1],maxfev=20000,cmap = "Blues",download_format = "None"):
        
        """
        statisticians
        ===================
        ### `statisticians(data,Tf = " ",ΔHf= " ",method="lm",p0_ma =[1,1,1],p0_vh =[1,1],p0_vhy =[1,1,1],p0_mw =[1,1],p0_bk=[1,1],maxfev=20000,cmap = "Blues",download_format = "None")`
        ----------------------------------------------------------------------------------------------------------------------------
        Method to show the table of statisticians of all models in a dataframe.

        -Mean Absolute Percentage Error (MAPE).
        -Root Mean Square Deviation (RMSD).
        -Akaike Information Criterion corrected (AICc).
        -Coefficient of Determination (R^2).
        -Adjusted Coefficient of Determination (R^2_a).

        Download in different formats the statisticians dataframe.
            
        ----------------------------------------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name.statisticians(data,Tf =500,download_format="tex")

        -------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Parameters 

        The explanation of the parameters of this method are presented below: 
        - ### data: 
        Dataset previously loaded according to the format of the standard table using the 
        funtion `dataset` .e.g. `data = dataset("/content/SMR-MeCN-MeOH.csv")`.
        Link to see the format of the standard table: https://da.gd/CAx7m.
        - ### Tf: 
        Value of the melting temperature in °K.
        - ### ΔHf: 
        Value of the enthalpy of fusion in °KJ/mol.
        - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
        Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
        for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
        work when the number of observations is less than the number of variables, use ‘trf’
        or ‘dogbox’ in this case.
        - ### p0: array_like, optional
        Initial guess for the parameters (length N). If None, then the initial values will 
        all be 1 (if the number of parameters for the function can be determined using 
        introspection, otherwise a ValueError is raised).
        The initial parameters according to the model are presented below:
        p0_ma, modified Apelblat model. Defaul is [1,1,1].
        p0_vh, van't Hoff model. Defautl is [1,1].
        p0_vhy, van't Hoff-Yaws model. Default is [1,1,1].
        p0_mw, modified Wilson model. Default is [1,1].
        p0_bk, Buchowski Ksiazaczak model.  Default is [1,1].     
        - ### maxfev: int, optional
        The maximum number of calls to the function. Default is 20000.
        - ### cmap: str or colormap
        Change the color of the color gradient according to matplotlib colormap.
        Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
        https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
        - ### download_format: {‘xlsx’, ‘csv’, ‘tex’}, optional
        Option to download the dataframe of statisticians in the chosen format, 
        excel format (‘xlsx’), comma separated values format (‘csv’), LaTeX format (‘tex’). 
        """
       
        names     = ["MAPE","RMSD","AICc","R2","R2_a"]
        names_tex = ["$MAPE$","$RMSD$","$AICc$","$R^2$","$R^2_{adj}$"]

        names_model =["statisticians"]
        names_modeltex = ["$Stat$"]

        std = []

        modelo_1 = model.modified_apelblat(self)
        std_1    = modelo_1.statisticians(method = method, p0 = p0_ma, maxfev=20000)["values"].values
        names_model.append("Apelblat")
        names_modeltex.append("$Apelblat$")
        std.append(std_1)

        modelo_2 = model.vant_hoff(self)
        std_2    = modelo_2.statisticians(method = method, p0 = p0_vh, maxfev=20000)["values"].values
        names_model.append("van't Hoff")
        names_modeltex.append("$van't \ Hoff$")
        std.append(std_2)

        modelo_3 = model.vant_hoff_yaws(self)
        std_3    = modelo_3.statisticians(method = method, p0 = p0_vhy, maxfev=20000)["values"].values
        names_model.append("Yaws")
        names_modeltex.append("$Yaws$")
        std.append(std_3)

        modelo_4 = model.modified_wilson(self)
        std_4    = modelo_4.statisticians(method = method, p0 = p0_mw, maxfev=20000)["values"].values
        names_model.append("Mod.Wilson")
        names_modeltex.append("$Mod.\ Wilson$")
        std.append(std_4)

        if Tf != " ":
            modelo_5 = model.buchowski_ksiazaczak(self,Tf)
            std_5    = modelo_5.statisticians(method = method, p0 = p0_bk, maxfev=20000)["values"].values
            names_model.append("λh")
            names_modeltex.append("$\lambda h$")
            std.append(std_5)


        idx = pd.IndexSlice
        slice_1 = idx[idx[3:], idx[names_model[1]:names_model[-1]]]
        slice_2 = idx[idx[:2], idx[names_model[1]:names_model[-1]]]

        df_estadis  = pd.DataFrame(dict(zip(names_model,[names]+std)))
        df_est = pd.DataFrame(dict(zip(names_modeltex,[names_tex]+std)))

        initial_cmap = cm.get_cmap(cmap)
        reversed_cmap=initial_cmap.reversed()
        
        dataframe = df_estadis.style.background_gradient(subset=slice_1,axis=1,cmap=initial_cmap)\
                                    .background_gradient(subset=slice_2,axis=1,cmap=reversed_cmap)\
                                  
        cols = df_estadis.columns
        name_archi = URL.split("/")[-1].split(".")[-2]
            
        nombre ="statisticians Models"
        extension = download_format

        if extension == "tex":
            if entorno == "/usr/bin/python3":
                url_13 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_est.to_latex(url_13,index=False,column_format= len(cols)*"c",escape =False)
                files.download(url_13)
            else:
                url_13 = nombre + "-"+ name_archi +"."+extension
                df_est.to_latex(url_13,index=False,column_format= len(cols)*"c",escape =False)
                files.download(url_13)

            environment_table(url_13)
            generate_pdf(nombre + "-"+ name_archi)

        if extension == "xlsx":  
            if entorno == "/usr/bin/python3" :
                url_13 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_estadis.to_excel(url_13,sheet_name=nombre)
                files.download(url_13)
            else:
                url_13 = nombre + "-"+ name_archi +"."+extension
                df_estadis.to_excel(url_13,sheet_name=nombre)

        if extension == "csv":   
            if entorno == "/usr/bin/python3":
                url_13 = "/content/"+ nombre + "-"+ name_archi +"."+extension
                df_estadis.to_csv(url_13)
                files.download(url_13)
            else:
                url_13 = nombre + "-"+ name_archi +"."+extension
                df_estadis.to_csv(url_13)

        return dataframe



    def plots(self,Tf = " ",ΔHf= " ",method="lm",p0_ma =[1,1,1],p0_vh =[1,1],p0_vhy =[1,1,1],p0_mw =[1,1],p0_bk=[1,1],p0_nrtl =[1,1,1,1,1,1],p0_w =[1,1,1,1,1,1],p0_wtp=[1,1],maxfev=20000,download_format = "pdf"):

        """
        plots
        ===================
        ### `plots(data,Tf = " ",ΔHf= " ",method="lm",p0_ma =[1,1,1],p0_vh =[1,1],p0_vhy =[1,1,1],p0_mw =[1,1],p0_bk=[1,1],maxfev=20000,download_format = "None")`
        ----------------------------------------------------------------------------------------------------------------------------
        Method to shows the graphs of calculated values and experimental values of solubility
        for all models. Download in different formats the graph.
            
        ----------------------------------------------------------------------------------------------------------------------------------
        # Examples
        >>> data = dataset("/content/SMR-MeCN-MeOH.csv") #upload data
        >>> model_name.plots(data,Tf =500,download_format="tex")

        -------------------------------------------------------------------------------------------------------------------------------------------------------
        ## Parameters 

        The explanation of the parameters of this method are presented below: 
        - ### data: 
        Dataset previously loaded according to the format of the standard table using the 
        funtion `dataset` .e.g. `data = dataset("/content/SMR-MeCN-MeOH.csv")`.
        Link to see the format of the standard table: https://da.gd/CAx7m.
        - ### Tf: 
        Value of the melting temperature in °K.
        - ### ΔHf: 
        Value of the enthalpy of fusion in °KJ/mol.
        - ### method: {‘lm’, ‘trf’, ‘dogbox’}, optional
        Method to use for optimization. See least_squares for more details. Default is ‘lm’ 
        for unconstrained problems and ‘trf’ if bounds are provided. The method ‘lm’ won’t 
        work when the number of observations is less than the number of variables, use ‘trf’
        or ‘dogbox’ in this case.
        - ### p0: array_like, optional
        Initial guess for the parameters (length N). If None, then the initial values will 
        all be 1 (if the number of parameters for the function can be determined using 
        introspection, otherwise a ValueError is raised).
        The initial parameters according to the model are presented below:
        p0_ma, modified Apelblat model. Defaul is [1,1,1].
        p0_vh, van't Hoff model. Defautl is [1,1].
        p0_vhy, van't Hoff-Yaws model. Default is [1,1,1].
        p0_mw, modified Wilson model. Default is [1,1].
        p0_bk, Buchowski Ksiazaczak model.  Default is [1,1].  
        - ### maxfev: int, optional
        The maximum number of calls to the function. Default is 20000.
        - ### cmap: str or colormap
        Change the color of the color gradient according to matplotlib colormap.
        Examples: "Greys","Purples","Blues",""Greens","Oranges","Reds", see also:
        https://matplotlib.org/stable/tutorials/colors/colormaps.html. Default is "Blues".
        - ### download_format: {‘pdf’, ‘png’,‘tex’}, optional
        Option to download the graph of calculated values and experimental values of solubility
        in pdf format (‘pdf’), png format (‘png’), LaTeX format (‘tex’).
        """



        nombre= "plot_models"
        name_archi ="-" + URL.split("/")[-1].split(".")[-2]
        
        if entorno == "/usr/bin/python3":
            url_15 = "/content/"+ nombre +  name_archi +".pdf"
            url_16 = "/content/"+ nombre +  name_archi +".png"
            url_17 = "/content/"+ nombre +  name_archi +".tex"
        else:
            url_15 = nombre +  name_archi +".pdf"
            url_16 = nombre +  name_archi +".png"
            url_17 = nombre +  name_archi +".tex"

        names_model = []
        names_model_tex = []
        L_cal       = []
        L_exp       = []
        L_R2a       = []

        modelo_1 = model.modified_apelblat(self)
        cal_1    = modelo_1.values(method=method,p0=p0_ma , maxfev=maxfev)["x3_Cal"].values
        exp_1    = modelo_1.values(method=method,p0=p0_ma , maxfev=maxfev)["x3_Exp"].values
        R2a_1    = modelo_1.statisticians(method = method, p0 = p0_ma, maxfev=20000)["values"][4]
        names_model.append("Modified Apelblat model")
        names_model_tex.append("Apelblat model")
        L_cal.append(cal_1) 
        L_exp.append(exp_1)
        L_R2a.append(R2a_1)

        modelo_2 = model.vant_hoff(self)
        cal_2    = modelo_2.values(method=method,p0=p0_vh , maxfev=maxfev)["x3_Cal"].values
        exp_2    = modelo_2.values(method=method,p0=p0_vh , maxfev=maxfev)["x3_Exp"].values
        R2a_2    = modelo_2.statisticians(method = method, p0 = p0_vh, maxfev=20000)["values"][4]
        names_model.append("van't Hoff model")
        names_model_tex.append("van't Hoff equation")
        L_cal.append(cal_2) 
        L_exp.append(exp_2)
        L_R2a.append(R2a_2)

        modelo_3 = model.vant_hoff_yaws(self)
        cal_3    = modelo_3.values(method=method,p0=p0_vhy , maxfev=maxfev)["x3_Cal"].values
        exp_3    = modelo_3.values(method=method,p0=p0_vhy , maxfev=maxfev)["x3_Exp"].values
        R2a_3    = modelo_3.statisticians(method = method, p0 = p0_vhy, maxfev=20000)["values"][4]
        names_model.append("van't Hoff-Yaws model")
        names_model_tex.append("Yaws model")
        L_cal.append(cal_3) 
        L_exp.append(exp_3)
        L_R2a.append(R2a_3)

        modelo_4 = model.modified_wilson(self)
        cal_4    = modelo_4.values(method=method,p0=p0_mw , maxfev=maxfev)["x3_Cal"].values
        exp_4    = modelo_4.values(method=method,p0=p0_mw , maxfev=maxfev)["x3_Exp"].values
        R2a_4    = modelo_4.statisticians(method = method, p0 = p0_mw, maxfev=20000)["values"][4]
        names_model.append("Modified Wilson model")
        names_model_tex.append("Modified Wilson model")
        L_cal.append(cal_4) 
        L_exp.append(exp_4)
        L_R2a.append(R2a_4)

        if Tf != " ":
            modelo_5 = model.buchowski_ksiazaczak(self,Tf)
            cal_5    = modelo_5.values(method=method,p0=p0_bk , maxfev=maxfev, )["x3_Cal"].values
            exp_5    = modelo_5.values(method=method,p0=p0_bk , maxfev=maxfev, )["x3_Exp"].values
            R2a_5    = modelo_5.statisticians(method = method, p0 = p0_bk, maxfev=20000)["values"][4]
            names_model.append("Buchowski-ksiazaczak λh model")
            names_model_tex.append("Buchowski-ksiazaczak " + "$\lambda h$"+ " model")
            L_cal.append(cal_5) 
            L_exp.append(exp_5)
            L_R2a.append(R2a_5)

        extension= download_format

        if extension != "tex":

            cols = 2
            rows = ceil(len(names_model)/cols)
                    
            L_r = []
            for i in range(1,rows+1):
                L_r += cols*[i]

                L_row =40*L_r
                L_col =40*list(range(1,cols+1))

            names = []
            for i in range(len(names_model)):
                names.append(names_model[i]+","+" R<sup>2</sup><sub>adj</sub> = "+ str(L_R2a[i].round(5)))


            fig = make_subplots(rows=rows, cols=cols,subplot_titles=names)
        
            for i in range(len(names_model)):
                fig.add_trace(go.Scatter(x=L_exp[i],y=L_cal[i],
                                            name = "",
                                            hovertemplate="x3_exp: %{x}<br>x3_cal: %{y}<br>",
                                            mode='markers',
                                            showlegend= False,
                                            marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))),
                                            row=L_row[i], col=L_col[i])
            
            for i in range(len(names_model)):
                X = np.linspace(min(L_cal[i]),max(L_cal[i]),200)
                fig.add_trace(go.Scatter(x=X,y=X,showlegend= False,marker=dict(size=6,line=dict(width=0.5,color="#2a3f5f")),hoverinfo = "skip"),row=L_row[i], col=L_col[i])

            for i in range(len(names_model)):
                fig.update_xaxes(title = "x<sub>3</sub><sup>Exp</sup>")

            for i in range(len(names_model)):
                fig.update_yaxes(title = "x<sub>3</sub><sup>Cal</sup>")
            
            fig.update_layout(title ="Solubility Model Graphs",height=100*len(names_model)+300, width= 1300,showlegend=False)

            fig.write_image(url_15,height=100*len(names_model)+300, width= 1300)
            fig.write_image(url_16,height=100*len(names_model)+300, width= 1300)


            grafica = fig.show()

            
        if extension == "tex":

            cols = 2
            rows = ceil(len(names_model)/cols)

            L_r = []
                    
            for i in range(0,rows):

                L_r += cols*[i]
                L_row =2*L_r
                L_col =4*list(range(0,cols))


            plt.rcParams["figure.figsize"] = (20,30)

            fig, axs = plt.subplots(rows, cols)

            for i in range(len(names_model)):
                x=L_exp[i]
                y=L_cal[i]

                axs[L_row[i], L_col[i]].scatter(x, y, c = "k",marker="v")
                axs[L_row[i], L_col[i]].set_title(names_model_tex[i],fontsize='large')
                axs[L_row[i], L_col[i]].set_xlabel(r'$x_3^{exp}$',fontsize=12)
                axs[L_row[i], L_col[i]].set_ylabel(r'$x_3^{cal}$',fontsize=12)

                axs[L_row[i], L_col[i]].xaxis.set_ticks_position('both')
                axs[L_row[i], L_col[i]].yaxis.set_ticks_position('both')
                axs[L_row[i], L_col[i]].tick_params(direction='in')

                X = [min(x),max(x)]
                Y = [min(y),max(y)]
                axs[L_row[i], L_col[i]].plot(X, Y,color='black',markersize=0.1)

            fig.subplots_adjust(hspace=0.5)

            tikzplotlib.save(url_17)
            grafica = plt.show()

            environment_graph_apart(url_17,cols,rows)
            generate_pdf(nombre +  name_archi)



        if entorno == "/usr/bin/python3":
                url= "/content/"+nombre + name_archi +"."+extension
                files.download(url)
        else:
                url= nombre + name_archi +"."+extension
                print(url)        

        return grafica

