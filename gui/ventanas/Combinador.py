# -*- coding: utf-8 -*-
"""
Módulo de la ventana de combinaciones
"""

import random

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import *
from PySide2.QtGui import QFont, QIcon, QPixmap
from PySide2.QtGui import QKeySequence, QStandardItem, QStandardItemModel
from PySide2.QtCore import Qt, Slot, QLocale, QItemSelectionModel

from util.Constants import *

# IL352 IL340 IL341 IG738 I5247


class Combinador(QDialog):
    null_icon = QIcon()
    applicationIcon = QIcon()

    def __init__(self, parent=None):
        super(Combinador, self).__init__(parent)

        if parent is not None:
            self.setParent(parent)

        # Propiedades de la ventana principal
        # ===================================
        # width = (self.screen().availableSize().width() // 16) * 8
        # height = (self.screen().availableSize().height() // 16) * 8
        width = 700
        height = 500
        self.resize(width, height)
        self.setWindowTitle("Combinador de horarios")

        # Por ahora es solo en español, cuando tenga ganas implemento algún sistema de traducción
        self.setLocale(QLocale.Spanish)

        # Layout del diálogo
        self.dialogLayout = QVBoxLayout(self)

        self._createControls(self)
        # self.dialogLayout.addStretch()
        self._createFooter()
        # self._cargarPreferencias()
        # self.centerToParent()

    def _createControls(self, parent):
        """Genera los controles principales de la ventana"""
        # Contenedores
        # ============

        # Widget principal
        self.pagina = QSplitter(parent)
        self.pagina.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Donde se muestra el horario
        self.schedule = QSplitter(self.pagina)
        self.schedule.setOrientation(Qt.Orientation.Vertical)

        # Controles
        # =========

        # Lista/selector de combinaciones
        # ...............................

        self.listCombinations = QListWidget(self.pagina)
        self.listCombinations.setMaximumWidth(100)
        # TODO: self.actualHorarioCambio()
        # self.listCombinations.currentItemChanged.connect(self.actualHorarioCambio)

        for x in range(20):
            self.listCombinations.addItem(str(x + 1))

        # Vista previa del horario
        # ........................

        self.schedulePreview = QTableView(self.schedule)
        self.schedulePreview.setTabKeyNavigation(False)
        self.modelPreview = QStandardItemModel(15, 6, self.schedulePreview)
        self.modelPreview.setHorizontalHeaderLabels([
            "Lunes", "Martes", "Miércoles",
            "Jueves", "Viernes", "Sábado",
        ])
        self.modelPreview.setVerticalHeaderLabels([
            "7:00 am",  "8:00 am", "9:00 am", "10:00 am",
            "11:00 am", "12:00 pm", "1:00 pm", "2:00 pm",
            "3:00 pm",  "4:00 pm", "5:00 pm", "6:00 pm",
            "7:00 pm",  "8:00 pm", "9:00 pm",
        ])
        for row in range(15):
            for column in range(6):
                texto = random.choice([
                    "", "", "", "IL352", "IL340", "IL341", "IG738", "I5247"
                ])
                color = random.choice([
                    "red", "blue", "green", "yellow", "orange", "magenta",
                    "cyan", "black", "gray", "brown", "purple"
                ])
                foreground = QtGui.QBrush(QtGui.QColor(color))
                item = QStandardItem(texto)
                item.setForeground(foreground)
                item.setFont(QtGui.QFont("Helvetica", pointSize=10, weight=QtGui.QFont.Black, italic=True))
                item.setEditable(False)
                self.modelPreview.setItem(row, column, item)

        self.schedulePreview.setModel(self.modelPreview)

        # Detalles del horario seleccionado
        # .................................

        self.scheduleDetails = QTableView(self.schedule)
        self.scheduleDetails.setTabKeyNavigation(False)

        self.modelDetails = QStandardItemModel(0, 6, self.scheduleDetails)
        self.modelDetails.setHorizontalHeaderLabels([
            "NRC", "Clave", "Materia", "Profesor",
            "Cupo", "Sección", "Periodo",
        ])
        self.modelDetails.appendRow([
            QStandardItem("189660"),
            QStandardItem("IG738"),
            QStandardItem("PRECALCULO"),
            QStandardItem("JOSE SOLIS ROGRIGUEZ"),
            QStandardItem("8/20"),
            QStandardItem("D05"),
            QStandardItem("16/01/22 - 15/07/22"),
        ])
        self.scheduleDetails.setModel(self.modelDetails)

        # Distibución de controles en los widgets
        # =======================================

        self.schedule.addWidget(self.schedulePreview)
        self.schedule.addWidget(self.scheduleDetails)

        self.pagina.addWidget(self.listCombinations)
        self.pagina.addWidget(self.schedule)

        self._addWidgetToScreen(self.pagina)

    def _createFooter(self):
        """Genera el pie de la ventana"""
        self.footer = QWidget(self)
        self.footerGrid = QHBoxLayout(self.footer)

        self.btnPrint = QPushButton("Imprimir", self.footer)
        self.btnClose = QPushButton("Cerrar", self.footer)

        # self.btnPrint.clicked.connect(self.imprimirHorario)
        self.btnClose.clicked.connect(self.close)

        self.footerGrid.addStretch()
        self.footerGrid.addWidget(self.btnPrint)
        self.footerGrid.addWidget(self.btnClose)

        self._addWidgetToScreen(self.footer)

    def _addWidgetToScreen(self, widget: QWidget):
        self.dialogLayout.addWidget(widget)
        self.setLayout(self.dialogLayout)


"""
package gui;

import jasperReports.JasperFacade;

import java.awt.BorderLayout;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.print.PageFormat;
import java.awt.print.Printable;
import java.awt.print.PrinterException;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;

import javax.swing.AbstractListModel;
import javax.swing.JButton;
import javax.swing.JInternalFrame;
import javax.swing.JList;
import javax.swing.JPanel;
import javax.swing.JProgressBar;
import javax.swing.JScrollPane;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.event.InternalFrameAdapter;
import javax.swing.event.InternalFrameEvent;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.table.AbstractTableModel;

import carga.Grupo;
import carga.Maestro;
import carga.Materia;

import combinacion.ModCombListener;
import combinacion.ModeloCombinatorio;
import combinacion.Solucion;

class CombListModel extends AbstractListModel
{
    static final long serialVersionUID = 1;
    ModeloCombinatorio mc;

    public CombListModel(ModeloCombinatorio mc)
    {
        super();
        this.mc = mc;
    }

    public Object getElementAt(int index)
    {
        return Integer.toString(index + 1);
    }

    public int getSize()
    {
        return mc.getSolCount();
    }

    public void fireIntervalAdded(Object source, int index0, int index1)
    {

        super.fireIntervalAdded(source, index0, index1);
    }
}

public class Combinador extends JInternalFrame implements ModCombListener, Printable
{
    static final long serialVersionUID = 1;

    ModeloCombinatorio mc;
    AbstractTableModel tm;
    AbstractTableModel tmGrupos;
    Solucion sol;
    CombListModel lm;
    JList solList;
    JProgressBar pb;

    public void nuevaSolucion(Solucion s)
    {
        sol = s;
        tm.fireTableDataChanged();
        tmGrupos.fireTableDataChanged();
    }

    public void imprimir() 
    {
        if (sol!=null)
        {
            char letras[]={'a','b','c','d','e','f'};
            Hashtable<String, Object> params = new Hashtable<String, Object>();
            
            for (int columnIndex=1;columnIndex<=6;columnIndex++)
            {
                for (int rowIndex=0;rowIndex<15;rowIndex++)
                {
                    String desc=sol.getDescripcionGrupo(columnIndex-1,rowIndex+7);
                    if (desc!=null)
                    {
                        params.put(letras[columnIndex-1]+""+(rowIndex+1),desc);
                    }
                }
            }
            
            ArrayList<String> header = new ArrayList<String>();
            header.add("clave");
            header.add("nrc");
            header.add("seccion");
            header.add("materia");
            header.add("maestro");
            header.add("periodo");

            
            List<List<Object>> values = new ArrayList<List<Object>>();
                        
            for (int x=0;x<sol.getNumGrupos();x++)
            {
                Object objGrupo=sol.getGrupo(x);
                
                ArrayList<Object> row = new ArrayList<Object>();

                Grupo grupo=(Grupo)objGrupo;
                row.add(grupo.getPadre().getPadre().getMateriaSiiau().getClave());
                row.add(grupo.getNrc());
                row.add(grupo.getSec());
                row.add(grupo.getPadre().getPadre().getNombre());
                row.add(grupo.getPadre().getNombre());
                row.add(grupo.horario.getPeriodoString());
                
                values.add(row);
            }
            
            
            try
            {
                JasperFacade.runReport("horario",params, header, values);
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }

        }
        /*
         * PrinterJob printJob = PrinterJob.getPrinterJob();
         * printJob.setJobName("Horario de Alumno"); printJob.setPrintable(this);
         * 
         * if (printJob.printDialog()) try { System.out.println("Calling
         * PrintJob.print()"); printJob.print(); System.out.println("End
         * PrintJob.print()"); } catch (PrinterException pe) {
         * System.out.println("Error printing: " + pe); }
         */
    }

    public int print(Graphics g, PageFormat pf, int pageIndex) throws PrinterException
    {
        int response = NO_SUCH_PAGE;
        Graphics2D g2 = (Graphics2D) g;
        // for faster printing, turn off double buffering
        // disableDoubleBuffering(this);
        Dimension d = this.getSize(); // get size of document
        double panelWidth = d.width; // width in pixels
        double panelHeight = d.height; // height in pixels
        double pageHeight = pf.getImageableHeight(); // height of printer page
        double pageWidth = pf.getImageableWidth(); // width of printer page
        double scale = pageWidth / panelWidth;
        int totalNumPages = (int) Math.ceil(scale * panelHeight / pageHeight);
        // make sure not print empty pages
        if (pageIndex >= totalNumPages)
        {
            response = NO_SUCH_PAGE;
        }
        else
        {
            // shift Graphic to line up with beginning of print-imageable region
            g2.translate(pf.getImageableX(), pf.getImageableY());
            // shift Graphic to line up with beginning of next page to print
            g2.translate(0f, -pageIndex * pageHeight);
            // scale the page so the width fits...
            g2.scale(scale, scale);
            this.paint(g2); // repaint the page for printing
            // enableDoubleBuffering(componentToBePrinted);
            response = Printable.PAGE_EXISTS;
        }
        return response;
    }

    public void progreso(String estado, int porcentaje)
    {

        if (porcentaje == -2)
        {
            pb.setIndeterminate(true);
            pb.setString(estado);
        }
        else
        {
            pb.setIndeterminate(false);
            if (porcentaje > -1)
                pb.setValue(porcentaje);

            if (porcentaje > -1)
                pb.setString(estado + ".." + Integer.toString(porcentaje) + "%");
            else
                pb.setString(estado + ".." + Integer.toString(pb.getValue()) + "%");

            if (porcentaje == -3)
            {
                if (mc.getSolCount() > 0)
                    lm.fireIntervalAdded(this, 0, mc.getSolCount() - 1);
            }
        }
    }

    public Combinador(ModeloCombinatorio mcomb)
    {
        sol = null;
        this.mc = mcomb;
        mc.addModCombListener(this);
        setTitle("Apeiron [Combinador]");
        setResizable(true);
        setMaximizable(true);
        setClosable(true);

        setDefaultCloseOperation(DISPOSE_ON_CLOSE);
        
        addInternalFrameListener(new InternalFrameAdapter(){
            @Override
            public void internalFrameClosed(InternalFrameEvent arg0)
            {
               mc.terminar();
            }
        });
        
        lm = new CombListModel(mc);

        solList = new JList(lm);
        solList.addListSelectionListener(new ListSelectionListener()
        {
            public void valueChanged(ListSelectionEvent e)
            {
                sol = mc.getSol(solList.getSelectedIndex());
                tm.fireTableDataChanged();
                tmGrupos.fireTableDataChanged();
            }
        });

        tm = new AbstractTableModel()
        {
            static final long serialVersionUID = 1;

            public int getColumnCount()
            {
                return 7;
            }

            public int getRowCount()
            {
                return 15;
            }

            public Object getValueAt(int rowIndex, int columnIndex)
            {
                if (columnIndex == 0)
                {
                    switch (rowIndex)
                    {
                    case 0:
                        return "7:00 am";
                    case 1:
                        return "8:00 am";
                    case 2:
                        return "9:00 am";
                    case 3:
                        return "10:00 am";
                    case 4:
                        return "11:00 am";
                    case 5:
                        return "12:00 pm";
                    case 6:
                        return "1:00 pm";
                    case 7:
                        return "2:00 pm";
                    case 8:
                        return "3:00 pm";
                    case 9:
                        return "4:00 pm";
                    case 10:
                        return "5:00 pm";
                    case 11:
                        return "6:00 pm";
                    case 12:
                        return "7:00 pm";
                    case 13:
                        return "8:00 pm";
                    case 14:
                        return "9:00 pm";
                    }
                }
                if (sol != null)
                {
                    String desc=sol.getDescripcionGrupo(columnIndex-1,rowIndex+7);
                    if (desc!=null)
                    {
                        return desc;
                    }
                    return "";
                }
                else
                    return "";
            }

            public String getColumnName(int column)
            {
                switch (column)
                {
                case 0:
                    return "Hora/Dia";
                case 1:
                    return "Lunes";
                case 2:
                    return "Martes";
                case 3:
                    return "Miércoles";
                case 4:
                    return "Jueves";
                case 5:
                    return "Viernes";
                case 6:
                    return "Sábado";
                }
                return "";
            }
        };

        JTable horario = new JTable(tm);

        JButton empezar = new JButton("Detener");
        empezar.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                ((JButton) e.getSource()).setEnabled(false);
                mc.abortar();
                lm.fireIntervalAdded(this, 0, mc.getSolCount() - 1);
            }
        });

        JButton btnImprimir = new JButton("Imprimir");
        btnImprimir.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                imprimir();
            }
        });

        JButton cerrar = new JButton("Cerrar");
        cerrar.addActionListener(new ActionListener()
        {
            public void actionPerformed(ActionEvent e)
            {
                dispose();
            }
        });

        getContentPane().setLayout(new BorderLayout());

        JSplitPane sp = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT, new JScrollPane(solList), new JScrollPane(horario));
        sp.setDividerLocation(100);
        sp.setOneTouchExpandable(true);

        pb = new JProgressBar(0, 100);
        pb.setStringPainted(true);

        JPanel p1 = new JPanel(new BorderLayout(), true);
        p1.add(empezar, "East");
        p1.add(pb, "Center");

        JPanel p2 = new JPanel(new FlowLayout(FlowLayout.RIGHT), true);
        p2.add(btnImprimir);
        p2.add(cerrar);

        tmGrupos = new AbstractTableModel()
        {
            static final long serialVersionUID = 1;

            public int getColumnCount()
            {
                return 7;
            }

            public int getRowCount()
            {
                if (sol != null)
                    return sol.getNumGrupos();
                else
                    return 0;
            }

            public Object getValueAt(int rowIndex, int columnIndex)
            {
                if (sol != null)
                {
                    Grupo grp = (Grupo) sol.getGrupo(rowIndex);
                    Maestro mae = grp.getPadre();
                    Materia mat = mae.getPadre();
                    switch (columnIndex)
                    {
                    case 0:
                        return mat.getMateriaSiiau().getClave();
                    case 1:
                        return grp.getNrc();
                    case 2:
                        return mat.getNombre();
                    case 3:
                        return mae.getNombre();
                    case 4:
                        return Integer.toString(grp.getDis()) + "/" + Integer.toString(grp.getCup());
                    case 5:
                        return grp.getSec();
                    case 6:
                        return grp.horario.getPeriodoString();
                    }
                    return null;
                }
                else
                    return null;
            }

            public String getColumnName(int column)
            {
                switch (column)
                {
                case 0:
                    return "Clave";
                case 1:
                    return "NRC";
                case 2:
                    return "Materia";
                case 3:
                    return "Maestro";
                case 4:
                    return "Cupo";
                case 5:
                    return "Sección";
                case 6:
                    return "Periodo";
                }
                return "";
            }
        };

        JPanel p3 = new JPanel(new BorderLayout());
        JTable tblGrupos = new JTable(tmGrupos);
        tblGrupos.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);
        tblGrupos.getColumnModel().getColumn(0).setPreferredWidth(70);
        tblGrupos.getColumnModel().getColumn(1).setPreferredWidth(70);
        tblGrupos.getColumnModel().getColumn(2).setPreferredWidth(300);
        tblGrupos.getColumnModel().getColumn(3).setPreferredWidth(300);
        tblGrupos.getColumnModel().getColumn(4).setPreferredWidth(100);
        tblGrupos.getColumnModel().getColumn(5).setPreferredWidth(100);
        tblGrupos.getColumnModel().getColumn(6).setPreferredWidth(200);

        p3.add(p2, "South");
        p3.add(new JScrollPane(tblGrupos), "Center");

        JSplitPane sp2 = new JSplitPane(JSplitPane.VERTICAL_SPLIT, sp, p3);
        sp2.setOneTouchExpandable(true);
        sp2.setDividerLocation(250);

        getContentPane().add(sp2, "Center");
        getContentPane().add(p1, "North");

        setSize(730, 500);
    }

    public void empezar()
    {
        mc.start();
    }
}

"""
