# -*- coding: utf-8 -*-
"""
Clase SolucionConPeriodo para administrar una posibilidad de acomodo de horario (considerando el periodo)
TODO: Convertir este Java a Python
"""

"""
package combinacion;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.Hashtable;
import java.util.Vector;

import carga.Grupo;
import carga.Horario;
import carga.Periodo;

public class SolucionConPeriodo extends Solucion
{
	protected Vector<Horario> horarios=new Vector<Horario>();
	Horario h=new Horario();
	ArrayList<Date> horas=new ArrayList<Date>();
	Hashtable<Date,Integer> horasCount=new Hashtable<Date, Integer>();
	
	private void agregarPeriodo(Periodo periodo)
	{
	   Date ini=periodo.getInicio();
	   boolean reordenar1=agregarHora(ini);
   	
   	Date fin=periodo.getFin();
   	boolean reordenar2=agregarHora(fin);
   	
   	if (reordenar1 || reordenar2)
   	{
   		Collections.sort(horas);
   	}
	}
	
	private void quitarPeriodo(Periodo periodo)
	{
	   Date ini=periodo.getInicio();
	   quitarHora(ini);
   	
   	Date fin=periodo.getFin();
   	quitarHora(fin);
	}
	
	private boolean agregarHora(Date date)
	{
		boolean reordenar=false;
		
		if (!horas.contains(date))
   	{
   		horas.add(date);
   		reordenar=true;
   	}
   	
   	incrementarCuenta(date);
   	return reordenar;
	}
	
	private void quitarHora(Date date)
	{
		boolean remove=decrementarCuenta(date);
		if (remove)
		{
			horas.remove(date);
		}
	}
	
	private void incrementarCuenta(Date date)
	{
		Integer cuenta=horasCount.get(date);
   	if (cuenta==null)
   	{
   		horasCount.put(date,new Integer(1));
   	}
   	else
   	{
   		horasCount.put(date,new Integer(cuenta+1));
   	}
	}
	
	private boolean decrementarCuenta(Date date)
	{
		boolean remove=false;
		
		Integer cuenta=horasCount.get(date);
   	if (cuenta!=null)
   	{
   		int nuevaCuenta=cuenta-1;
   		if (cuenta<=0)
   		{
   			horasCount.remove(date);
   			remove=true;
   		}
   		else
   		{
   			horasCount.put(date,new Integer(nuevaCuenta));
   		}
   	}
   	
   	return remove;
	}
	
	@Override
	public void agregar(Grupo g)
	{
	   super.agregar(g);
	   horarios.add(g.horario);
	   agregarPeriodo(g.horario.getPeriodo());
	}
	
	@Override
	public void quitar(Grupo g)
	{
	   super.quitar(g);
	   horarios.remove(g.horario);
	   quitarPeriodo(g.horario.getPeriodo());
	}
	
	@Override
	public boolean compatible(Horario h)
	{
	   for (Horario horario:horarios)
	   {
	   	if (!compatible(horario,h))
	   	{
	   		return false;
	   	}
	   }
	   return true;
	}
	
	@Override
	public int getHuecos()
	{
	   int huecos=0;
	   for (int x=0;x<horas.size()-1;x++)
	   {
	   	Date inicio=horas.get(x);
	   	Date fin=horas.get(x+1);
	   	h.limpiar();
	   	
	   	for (Horario horario:horarios)
		   {
	   		if (horario.getPeriodo().estaDentroDe(inicio,fin))
	   		{
	   			h.agregar(horario);
	   		}
		   }
	   	huecos+=h.getHuecos();
	   }
	   
	   return huecos;
	}

	@Override
	public int getHuecos(Grupo g)
	{
		horarios.add(g.horario);
		agregarPeriodo(g.horario.getPeriodo());
		
		int huecos=getHuecos();
		
		quitarPeriodo(g.horario.getPeriodo());
		horarios.remove(g.horario);
		
		return huecos;
	}
	
	@SuppressWarnings("unchecked")
   @Override
	public Object clone()
	{
		SolucionConPeriodo solucion=(SolucionConPeriodo)super.clone();
		solucion.horarios=(Vector<Horario>)horarios.clone();
		return solucion;
	}
	
	@Override
	protected Solucion crearSolucion()
	{
	   return new SolucionConPeriodo();
	}
	
	protected boolean compatible(Horario h, Horario h2)
	{
		boolean horarioCompatible= h2.compatible(h);
		boolean periodoCompatible= isPeriodoCompatible(h,h2);
		
		return horarioCompatible || periodoCompatible;
	}
	
	protected boolean isPeriodoCompatible(Horario h, Horario h2)
	{
		if (h==null || h2==null)
		{
			return false;
		}
		
		return h.getPeriodo().compatible(h2.getPeriodo());
	}
	
	@Override
	public String getDescripcionGrupo(int idx1, int idx2)
	{
		int count=0;
		StringBuffer sb=new StringBuffer();
		for (int x=0;x<horarios.size();x++)
		{
			Horario horario=horarios.get(x);
			
			if (horario.getHora(idx1, idx2))
			{
				if (count>0)
				{
					sb.append(",");
				}

				Grupo g=grupos.get(x);
				sb.append(g.getPadre().getPadre().getMateriaSiiau().getClave());
				
				count++;
			}
		}
		
		if (sb.length()>0)
		{
			return sb.toString();
		}
		return null;
	}
}
"""