# -*- coding: utf-8 -*-
"""
@author: juanes
"""
import time as t 
from tkinter import *
import tkinter.messagebox as mb  
import tkinter.ttk as ttk 
import mysql.connector as sqlbd
import tkinter as tk 
dbConexion = sqlbd.connect(
    host='localhost',
    user="root",  
    password="sqlPass11", #Esto cambia según tu configuración.   
    database='ica'
)
#Creamos el cursor:
dbCursor = dbConexion.cursor(buffered=True)
class IcaApp(tk.Tk):
    def __init__(self):
        #Definimos la interfaz
        super().__init__()
        #Título de la ventana
        self.title('Sistema CRUD - Ica')
        #Tamaño.
        self.geometry("800x650+351+174")  
        #Labels 
        self.lblTitle = tk.Label(self, text="CRUD - Índice de calidad.", font=("Helvetica", 16), bg="yellow", fg="green")  
        self.lblID = tk.Label(self, text="ID:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblOD = tk.Label(self, text="Oxígeno D:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblSST = tk.Label(self, text="Sólidos ST:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblDQO = tk.Label(self, text="Demanda QO:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblCE = tk.Label(self, text="Conductividad eléct.:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblPH = tk.Label(self, text="pH:", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblSelect = tk.Label(self, text="Seleccione un registro para eliminar o actualizar", font=("Helvetica", 10), bg="blue", fg="yellow")  
        self.lblSearch = tk.Label(self, text="ID a consultar: ",font=("Helvetica", 10), bg="blue", fg="yellow")  
        #Cajas de texto.
        self.entID = tk.Entry(self)  
        self.entOD = tk.Entry(self)  
        self.entSST = tk.Entry(self)  
        self.entDQO = tk.Entry(self)  
        self.entCE = tk.Entry(self)  
        self.entPH = tk.Entry(self)
        self.entSearch = tk.Entry(self)  
        #Botones
        self.btn_register = tk.Button(self, text="Registrar", font=("Helvetica", 11), bg="yellow", fg="blue",command=self.Insert_variables)  
        self.btn_update = tk.Button(self,text="Actualizar",font=("Helvetica",11),bg="yellow", fg="blue",command=self.updateData)  
        self.btn_delete = tk.Button(self, text="Eliminar", font=("Helvetica", 11), bg="yellow", fg="blue",command=self.delete_data)  
        self.btn_clear = tk.Button(self, text="Limpiar", font=("Helvetica", 11), bg="yellow", fg="blue",command=self.limpiarCampos)  
        self.btn_show_all = tk.Button(self, text="Mostrar todos", font=("Helvetica", 11), bg="yellow", fg="blue",command=self.load__data)  
        self.btn_search = tk.Button(self, text="Buscar", font=("Helvetica", 11), bg="yellow", fg="blue",command=self.showSearch)  
        self.btn_exit = tk.Button(self, text="Salir", font=("Helvetica", 16), bg="yellow", fg="blue",command=self.exit)  
        #Tabla - visualización de registros:
        columns = ("#1", "#2", "#3", "#4", "#5", "#6", "#7","#8","#9")
        self.tvReg= ttk.Treeview(self,show="headings",height="5", columns=columns)  
        self.tvReg.heading('#1', text='ID', anchor='center')  
        self.tvReg.column('#1', width=60, anchor='center', stretch=False)  
        self.tvReg.heading('#2', text='Oxígeno disuelto', anchor='center')  
        self.tvReg.column('#2', width=20, anchor='center', stretch=True)  
        self.tvReg.heading('#3', text='SST', anchor='center')  
        self.tvReg.column('#3',width=20, anchor='center', stretch=True)  
        self.tvReg.heading('#4', text='Demanda Quim. O.', anchor='center')  
        self.tvReg.column('#4',width=20, anchor='center', stretch=True)  
        self.tvReg.heading('#5', text='CE', anchor='center')  
        self.tvReg.column('#5',width=20, anchor='center', stretch=True)  
        self.tvReg.heading('#6', text='pH', anchor='center')  
        self.tvReg.column('#6', width=10, anchor='center', stretch=True)  
        self.tvReg.heading('#7', text='Índice de calidad', anchor='center')  
        self.tvReg.column('#7', width=20, anchor='center', stretch=True)
        self.tvReg.heading('#8', text='Calidad agua', anchor='center')  
        self.tvReg.column('#8', width=20, anchor='center', stretch=True)
        self.tvReg.heading('#9', text='Señal alerta', anchor='center')  
        self.tvReg.column('#9', width=20, anchor='center', stretch=True)
        #Barras de desplazamiento para la tabla:
        vsb= ttk.Scrollbar(self, orient=tk.VERTICAL,command=self.tvReg.yview)  
        vsb.place(x=40 + 640 + 1, y=310, height=180 + 20)  
        self.tvReg.configure(yscroll=vsb.set)  
        hsb = ttk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.tvReg.xview)  
        hsb.place(x=40 , y=310+200+1, width=620 + 20) 
        self.tvReg.configure(xscroll=hsb.set)  
        self.tvReg.bind("<<TreeviewSelect>>", self.mostrarRegistroSeleccionado)
        #Ubicación de cada componente:
        #Labels
        self.lblTitle.place(x=280, y=30, height=27, width=300)  
        self.lblID.place(x=175, y=70, height=23, width=100)  
        self.lblOD.place(x=175, y=100, height=23, width=100)  
        self.lblSST.place(x=171, y=129, height=23, width=104)  
        self.lblDQO.place(x=171, y=158, height=23, width=65)  
        self.lblCE.place(x=171, y=187, height=23, width=71)  
        self.lblPH.place(x=171, y=217, height=23, width=128)  
        self.lblSelect.place(x=150, y=280, height=23, width=400)  
        self.lblSearch.place(x=174, y=560, height=23, width=134)  
        #Cajas de texto
        self.entID.place(x=277, y=72, height=21, width=186)  
        self.entOD.place(x=277, y=100, height=21, width=186)  
        self.entSST.place(x=277, y=129, height=21, width=186)  
        self.entDQO.place(x=277, y=158, height=21, width=186)  
        self.entCE.place(x=278, y=188, height=21, width=195)  
        self.entPH.place(x=278, y=218, height=21, width=90)  
        self.entSearch.place(x=310, y=560, height=21, width=186)  
        #Botones
        self.btn_register.place(x=290, y=245, height=25, width=76)  
        self.btn_update.place(x=370, y=245, height=25, width=76)  
        self.btn_delete.place(x=460, y=245, height=25, width=76)  
        self.btn_clear.place(x=548, y=245, height=25, width=76)  
        self.btn_show_all.place(x=630, y=245, height=25, width=76)  
        self.btn_search.place(x=498, y=558, height=26, width=60)  
        self.btn_exit.place(x=320, y=610, height=31, width=60)  
        #Tabla
        self.tvReg.place(x=40, y=310, height=200, width=640)
        #Habilitar campos:
        self.entID.config(state="normal")
        self.entOD.config(state="normal")
        self.entSST.config(state="normal")
        self.entDQO.config(state="normal")
        self.entCE.config(state="normal")
        self.entPH.config(state="normal")
        #Métodos carga
        self.load__data()
        self.createtable()
    def exit(self):  
        MsgBox = mb.askquestion('SALIR', '¿Está seguro que desea salir de la aplicación?', icon='warning')  
        if MsgBox == 'yes':  
            self.destroy()  
    def delete_data(self):  
        Id = self.entID.get()
        MsgBox = mb.askquestion('Eliminar', '¿Está seguro que desea eliminar el registro seleccionado?', icon='warning')  
        if MsgBox == 'yes':  
            if dbConexion.connect() == False:  
                dbConexion.connect()  
                try:
                    dbCursor.execute("use ica")  
                    Delete = "delete from variables_ica where Id=%d" %(Id)
                    dbCursor.execute(Delete)  
                    dbConexion.commit()  
                    mb.showinfo("Información", "Registro eliminado satisfactoriamente.")  
                except sqlbd.Error as err: 
                    print(err)
                    dbConexion.rollback()
                    mb.showerror("Error","No se pudo borrar el registro, intente de nuevo.")
                finally:
                        dbConexion.close()
        self.load__data()  
        self.limpiarCampos()
    def limpiarCampos(self):   
        self.entID.delete(0, tk.END)  
        self.entOD.delete(0, tk.END)  
        self.entDQO.delete(0, tk.END)  
        self.entSST.delete(0, tk.END)  
        self.entCE.delete(0, tk.END)  
        self.entPH.delete(0, tk.END)  
    def showSearch(self):
        if dbConexion.connect() == False:  
            dbConexion.connect()  
        idConsulta = self.entSearch.get()
        print(idConsulta)
        if idConsulta == "":
            mb.showerror("Error","El campo de búsqueda está vacío.")
            self.entSearch.focus_set()
            self.tvReg.delete(*self.tvReg.get_children()) # Limpía la tabla    
        dbCursor.execute("use ica")   
        sql_consulta = "SELECT* FROM variables_ica where Id=%d" %(int(idConsulta))  
        dbCursor.execute(sql_consulta)  
        filas_ = dbCursor.fetchall()
        #Inicializamos variables vacías, que contendrán los valores obtenidos en la consulta:
        idV =0
        oxigeno_disuelto = 0.0
        demandaQuimicadeOxigeno = 0.0
        solidos_suspendidosTot = 0.0
        conductividad_electrica_=0.0
        p_h_ = 0
        indice_calidad_ = 0.0
        aguaCalidad = ""
        alertaSennal =""
        #Recorremos la consulta, para después mostrarla en la tabla:
        for _fila in filas_:
            idV = _fila[0]
            oxigeno_disuelto = _fila[1]
            demandaQuimicadeOxigeno = _fila[2]
            solidos_suspendidosTot = _fila[3]
            conductividad_electrica_ = _fila[4]
            p_h_ = _fila[5]
            indice_calidad_ = _fila[6] 
            aguaCalidad = _fila[7]
            alertaSennal = _fila[8]
            self.tvReg.insert("",'end',text=idV,values=(oxigeno_disuelto,demandaQuimicadeOxigeno,solidos_suspendidosTot,conductividad_electrica_,p_h_,indice_calidad_,aguaCalidad,alertaSennal))
    def mostrarRegistroSeleccionado(self,event):
        self.limpiarCampos()
        #Recorre y captura valores de la fila seleccionada en la tabla
        for seleccion in self.tvReg.selection():
            item_ = self.tvReg.item(seleccion)
        iden,od,dqDo,sst_,ce,ph,ic,ac,alsenn=item_["values"][0:8]
        self.entID.insert(0,iden)
        self.entOD.insert(0,od)
        self.entDQO.insert(0,dqDo)
        self.entSST.insert(0,sst_)
        self.entCE.insert(0,ce)
        self.entPH.insert(0,ph)
        print(f"Índice de calidad: {ic}\n Calidad agua: {ac}\n Señal de alerta: {alsenn}")
    def createtable(self):  
        if dbConexion.connect == False:  
            dbConexion.connect()  
        dbCursor.execute("CREATE DATABASE IF NOT EXISTS ica") # Creamos una nueva base de datos llamada Ica (en caso que no exista).
        dbCursor.execute("use ica")  
        dbCursor.execute("create table if not exists variables_ica(Id bigint not null primary key,oxigenoDisuelto decimal not null,constraint chkOD check(oxigenoDisuelto >0.0),solidosSuspendidosT decimal not null,constraint chkSST check(solidosSuspendidosT >0.0),demandaQuiOxigeno decimal not null,constraint chkDQO check(demandaQuiOxigeno >0.0),conductividadElectrica decimal not null,constraint chkConduct check(conductividadElectrica > 0.0),pH int not null,indiceCalidad decimal not null,calidadAgua varchar(12) not null,sennalAlerta varchar(12) not null,constraint calidadAguaCheck check(calidadAgua IN('Muy mala','Mala','Regular','Aceptable','Buena')),constraint sennalAlertaCheck check(sennalAlerta IN('Rojo','Naranja','Amarillo','Verde','Azul')));")  
        dbConexion.commit() 
    def load__data(self):
        if dbConexion.connect == False:
            dbConexion.connect() 
        self.tvReg.delete(*self.tvReg.get_children())
        #Ejecutando sentencia de consulta:
        dbCursor.execute('use ica;')
        consulta = "select* from variables_ica"
        dbCursor.execute(consulta)
        totalReg = dbCursor.rowcount
        if totalReg == 0:
            t.sleep(2)
            mb.showinfo("Información","No hay registros para mostrar, por favor agregue datos.")
        print(f"Total registros: {totalReg}")
        filas_ = dbCursor.fetchall()
        #Inicializamos variables vacías, que contendrán los valores obtenidos en la carga:
        idV =0
        oxigeno_disuelto = 0.0
        demandaQuimicadeOxigeno = 0.0
        solidos_suspendidosTot = 0.0
        conductividad_electrica_=0.0
        p_h_ = 0
        indice_calidad_ = 0.0
        aguaCalidad = ""
        alertaSennal =""
        #Recorremos la consulta, para después mostrarla en la tabla:
        for _fila in filas_:
            idV = _fila[0]
            oxigeno_disuelto = _fila[1]
            demandaQuimicadeOxigeno = _fila[2]
            solidos_suspendidosTot = _fila[3]
            conductividad_electrica_ = _fila[4]
            p_h_ = _fila[5]
            indice_calidad_ = _fila[6] 
            aguaCalidad = _fila[7]
            alertaSennal = _fila[8]
            self.tvReg.insert("",'end',text=idV,values=(oxigeno_disuelto,demandaQuimicadeOxigeno,solidos_suspendidosTot,conductividad_electrica_,p_h_,indice_calidad_,aguaCalidad,alertaSennal))
    def updateData(self):
        calidad_agua=""
        sennalAlerta=""
        if dbConexion.connect() == False:
            dbConexion.connect()
        print('Actualizando registro...')
        t.sleep(2)
        dbCursor.execute('use ica;')
        #Capturamos los valores de las cajas de texto en variables:
        idReg =self.entID.get()
        oxigd = self.entOD.get()
        dqdo = self.entDQO.get()
        sst_ = self.entSST.get()
        ce_ = self.entCE.get()
        _ph = self.entPH.get()
        indiceCalidad_ = ((oxigd*0.2)+(dqdo*0.2)+(sst_*0.2)+(ce_*0.2)+(_ph*0.2))
        if indiceCalidad_ >= 0.00 and indiceCalidad_ <=0.25:
            calidad_agua="Muy mala"
            sennalAlerta="Rojo"
        elif indiceCalidad_ >=0.26 and indiceCalidad_ <=0.50:
            calidad_agua="Mala"
            sennalAlerta="Naranja"
        elif indiceCalidad_>=0.51 and indiceCalidad_ <=0.70:
            calidad_agua="Regular"
            sennalAlerta="Amarillo"
        elif indiceCalidad_ >=0.71 and indiceCalidad_ <=0.90:
            calidad_agua="Aceptable"
            sennalAlerta="Verde"
        elif indiceCalidad_ >=0.91 and indiceCalidad_ <=1.00:
            calidad_agua="Buena"
            sennalAlerta="Azul"
        
        if dbConexion.connect() == False:  
             dbConexion.connect()
        queryActualizacion = "update variables_ica set oxigenoDisuelto=%s,solidosSuspendidosT=%s,demandaQuiOxigeno=%s,conductividadElectrica=%s,pH=%f,indiceCalidad=%f,calidadAgua='%s',sennalAlerta='%s' where Id=%d;" % (oxigd,dqdo,sst_,ce_,_ph,indiceCalidad_,calidad_agua,sennalAlerta,idReg)
        dbCursor.execute(queryActualizacion)
        dbConexion.commit()
        t.sleep(1)
        mb.showinfo("Información","Registro seleccionado actualizado exitosamente.")
        self.load__data()
    def Insert_variables(self):
        #%s %f %d
        calidad_agua = ""
        sennalAlerta = ""
        indiceCalidad_ = 0.0
        if dbConexion.connect() == False:
            dbConexion.connect()
        #Obteniendo valores de las cajas de texto:
        Id_=self.entID.get()
        Od_ = self.entOD.get()
        Dqo_ = self.entDQO.get()
        Sst_ = self.entSST.get()
        Ce_ = self.entCE.get()
        Ph_ = self.entPH.get()
        #Validamos que las cajas de texto no estén vacías:
        if Id_ =="":
            mb.showinfo("Información","Digite ID")
            self.entID.focus_set()
            
        if Od_ =="":
            mb.showinfo("Información","Digite Oxígeno disuelto")
            self.entOD.focus_set()

        if Dqo_ =="":
            mb.showinfo("Información","Digite Demanda química de oxígeno.")
            self.entDQO.focus_set()

        if Sst_ =="":
            mb.showinfo("Información","Digite Sólidos suspendidos totales.")
            self.entSST.focus_set()

        if Ce_=="":
            mb.showinfo("Información","Digite conductividad eléctrica.")
            self.entCE.focus_set()

        if Ph_ == "":
            mb.showinfo("Información","Digite Ph")
            self.entPH.focus_set()
        #Para realizar dichas operaciones, se debe convertir a float:
        indiceCalidad_ = ((float(Od_)*0.2)+(float(Dqo_)*0.2)+(float(Sst_)*0.2)+(float(Ce_)*0.2)+(int(Ph_)*0.2))
        if indiceCalidad_ >= 0.0 and indiceCalidad_ <=0.25:
            calidad_agua="Muy mala"
            sennalAlerta="Rojo"
        elif indiceCalidad_ >=0.26 and indiceCalidad_ <=0.50:
            calidad_agua="Mala"
            sennalAlerta="Naranja"
        elif indiceCalidad_>=0.51 and indiceCalidad_ <=0.70:
            calidad_agua="Regular"
            sennalAlerta="Amarillo"
        elif indiceCalidad_ >=0.71 and indiceCalidad_ <=0.90:
            calidad_agua="Aceptable"
            sennalAlerta="Verde"
        elif indiceCalidad_ >=0.91 and indiceCalidad_ <=1.00:
            calidad_agua="Buena"
            sennalAlerta="Azul"
        if dbConexion.connect() == False:  
             dbConexion.connect()
        #Insertando los datos a la tabla:
        try:
            print(f'Nuevo registro: {Id_}')
            queryInsert = "insert into variables_ica(id,oxigenoDisuelto,solidosSuspendidosT,demandaQuiOxigeno,conductividadElectrica,pH,indiceCalidad,calidadAgua,sennalAlerta) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            dbCursor.execute(queryInsert,(Id_,Od_,Dqo_,Sst_,Ce_,Ph_,indiceCalidad_,calidad_agua,sennalAlerta))
            mb.showinfo("Información","Registro exitoso.")
            dbConexion.commit()
            self.load__data()
            self.limpiarCampos()
        except sqlbd.Error as err: 
            print(err)
            dbConexion.rollback()
            mb.showerror("Error","El registro ha fallado, intente de nuevo.")
        finally:
            dbConexion.close()
#Valida si es el método main.
if __name__=='__main__':
    #La variable toma el valor de la clase <<IcaApp>>
    aplicacionCrud = IcaApp()
    #Se llama la interfaz gráfica.
    aplicacionCrud.mainloop()    
        
        