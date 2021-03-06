# -*- coding: utf-8 -*-
"""
Módulo del modelo combinatorio PrimeroElMejor
"""

from carga.AdDatos import AdDatos
from carga.Grupo import Grupo
from combinacion.ModeloCombinatorio import ModeloCombinatorio


class PrimeroElMejor(ModeloCombinatorio):

    @staticmethod(comparadorDeGrupos)
    def comparadorDeGrupos(grupo1, grupo2):
        if grupo1.huecos > grupo2.huecos:
            return 1
        elif grupo1.huecos == grupo2.huecos:
            return 0
        else:
            return -1

    def __init__(self, datos: AdDatos):
        super(datos)

    def ponerMateria(self, s, indiceMat: int):
        if indiceMat >= len(materias):
            if len(materias) > 0:
                self.progreso += 1
                self.solCount += 1

                if total > 0:
                    self.fireProgreso(
                        f"[{self.solCount}] {self.progreso}/{round(self.total)}")
                else:
                    self.fireProgreso(
                        "Generando horarios ["+Integer.toString(solCount)+"]", -2)

                self.huecos = s.getHuecos()
                assert huecos <= maxHuecos

                sc = self.s.copy()

                if self.hashHuecos[huecos] == None:
                    self.hashHuecos[huecos] = []

                self.hashHuecos[huecos].append(sc)

                fireNuevaSolucion(sc)
        else:

            self.grupos = materias[indiceMat]

            # Calcular huecos
            for x, grupo in enumerate(self.grupos):
                if self.s.compatible(grupo.horario):
                    self.grupos[x].huecos = self.s.getHuecos(grupos[x])
                else:
                    self.grupos[x].huecos = 1000  # Infinito

            sorted(grupos, key=self.comparadorDeGrupos)

            # Empieza la combinacion
            for grupo in self.grupos:
                if abortar:
                    break

                self.salir = False

                if grupo.huecos >= 1000:  # Empiezan los no compatibles
                    self.salir = True

                if indiceMat < len(materias)-1:  # no es la ultima materia
                    if maxHuecosInt > -1 and grupo.huecos > maxHuecosInt:  # Condicion de no aceptacion
                        self.salir = True

                else:
                    if maxHuecos > -1 and grupo.huecos > maxHuecos:  # Condicion de no aceptacion
                        self.salir = True

                if maxHorarios > -1 and solCount >= maxHorarios:  # Se supero el limite
                    self.salir = True

                if self.salir:
                    if maxHorarios == -1:
                        tmp = len(self.grupos) - x

                        for m in range(indiceMat + 1, len(materias)):
                            tmp *= len(materias[m])

                        progreso += tmp

                        if total > 0:
                            self.fireProgreso(
                                f"[{self.solCount}] {self.progreso}/{self.total}", round(self.progreso * 100 // self.total))
                        else:
                            self.fireProgreso(
                                f"Generando horarios [{self.solCount}]", -2)

                    break

                self.s.agregar(grupos[x])
                self.ponerMateria(s, indiceMat+1)
                self.s.quitar(grupos[x])

    def combinar(self):
        comb = 1
        for z in range(len(materias)):
            comb *= len(materias[z])
            if comb < 0:  # Se desbordo
                break

        if maxHorarios > -1 and (maxHorarios < comb or comb < 0):
            total = maxHorarios
        else:
            total = comb

        progreso = 0

        if self.datos.evaluarPeriodos:
            ponerMateria(SolucionConPeriodo(), 0)
        else:
            ponerMateria(Solucion(), 0)

        if self.abortar:
            self.fireProgreso("Combinación cancelada", -1)
        else:
            self.fireProgreso("Combinación terminada", 100)


"""
package combinacion;

import java.util.Arrays;
import java.util.Comparator;
import java.util.Vector;

import carga.AdDatos;
import carga.Grupo;

public class PrimeroElMejor extends ModeloCombinatorio {
    
    private static Comparator<Grupo> comparadorDeGrupos=new Comparator<Grupo>()
    {
        public int compare(Grupo grupo1, Grupo grupo2)
        {
            if (grupo1.huecos>grupo2.huecos)
            {
                return 1;
            }
            else if (grupo1.huecos==grupo2.huecos)
            {
                return 0;
            }
            else
            {
                return -1;
            }
        }
    };
        
    public PrimeroElMejor(AdDatos datos)
    {
        super(datos);
    }
    
    private void ponerMateria(Solucion s,int indiceMat){

        if (indiceMat>=materias.length){
            if (materias.length>0){
                progreso++;
                solCount++;
            
                if (total>0)
                    fireProgreso("["+Integer.toString(solCount)+"] "+Long.toString(progreso)+"/"+Long.toString(total),Math.round(progreso*100/total));
                else
                    fireProgreso("Generando horarios ["+Integer.toString(solCount)+"]",-2);

                int huecos=s.getHuecos();
                assert huecos<=maxHuecos;
                
                Solucion sc=(Solucion)s.clone();
                
                if (hashHuecos[huecos]==None)
                {
                    hashHuecos[huecos]=new Vector();
                }
                hashHuecos[huecos].add(sc);
                
                fireNuevaSolucion(sc);
            }
        else:
            
            Grupo grupos[]=materias[indiceMat];
                    
            //Calcular huecos
            for (int x=0;x<grupos.length;x++){
                if (s.compatible(grupos[x].horario))
                {
                    grupos[x].huecos=s.getHuecos(grupos[x]);
                }
                else
                {
                    grupos[x].huecos=1000; //infinito
                }
            }
            
            Arrays.sort(grupos,comparadorDeGrupos);
            
            //Empieza la combinacion
            for (int x=0;x<grupos.length;x++){
                
                if (abortar)
                    break;
                
                boolean salir=False;
                
                if (grupos[x].huecos>=1000) //Empiezan los no compatibles
                    salir=True;
                
                
                if (indiceMat<materias.length-1){ //no es la ultima materia
                    if (maxHuecosInt>-1 && grupos[x].huecos>maxHuecosInt) //Condicion de no aceptacion 
                        salir=True;
                    
                else:
                    if (maxHuecos>-1 && grupos[x].huecos>maxHuecos) //Condicion de no aceptacion 
                        salir=True;
                }
                
                
                if (maxHorarios>-1 && solCount>=maxHorarios) //Se supero el limite
                    salir=True;
                
                if (salir){
                    if (maxHorarios==-1){
                        int tmp=grupos.length-x;
                        for (int m=indiceMat+1;m<materias.length;m++)
                            tmp*=materias[m].length;
                        progreso+=tmp;
                        
                        if (total>0)
                            fireProgreso("["+Integer.toString(solCount)+"] "+Long.toString(progreso)+"/"+Long.toString(total),Math.round(progreso*100/total));
                        else
                            fireProgreso("Generando horarios ["+Integer.toString(solCount)+"]",-2);
                    }
                    
                    break;
                }
                
                s.agregar(grupos[x]);
                ponerMateria(s,indiceMat+1);
                s.quitar(grupos[x]);
    
            }
        }
    }
    
    protected void combinar() {
        int comb=1;
        for(int z=0;z<materias.length;z++){
            comb*=materias[z].length;
            if (comb<0)//Se desbordo
                break;
        }
        if (maxHorarios>-1 && (maxHorarios<comb||comb<0))
            total=maxHorarios;
        else
            total=comb;
        progreso=0;
        
        if (datos.evaluarPeriodos)
        {
            ponerMateria(new SolucionConPeriodo(),0);
        }
        else
        {
            ponerMateria(new Solucion(),0);
        }
        
        if (abortar)
            fireProgreso("Combinación cancelada",-1);
        else
            fireProgreso("Combinación terminada",100);
        
    }

}

"""
