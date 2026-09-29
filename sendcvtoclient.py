#!/usr/bin/env python3
"""sendcvtoclient: calcula la tarifa a presentar al cliente para un perfil
con salario bruto anual en España.

Uso:
    python3 sendcvtoclient.py 65000
    python3 sendcvtoclient.py 65000 --margin 0.30 --utilization 0.9
"""
import argparse

# Supuestos 2026 (revisar): base máxima de cotización mensual y
# cotización a cargo de la empresa (CC 23,60 + desempleo 5,50 + FOGASA 0,20
# + FP 0,60 + MEI 0,75 + AT/EP ~1,50).
BASE_MAX_MENSUAL = 5101.20
SS_EMPRESA = 0.3215


def calcular(bruto, margin, overhead, utilization, work_days, ss_rate, pagas):
    base_anual = min(bruto, BASE_MAX_MENSUAL * 12)
    ss = base_anual * ss_rate
    coste_empresa = bruto + ss
    coste_total = coste_empresa * (1 + overhead)
    dias_facturables = work_days * utilization
    coste_dia = coste_total / dias_facturables
    tarifa_dia = coste_dia / (1 - margin)
    return {
        "bruto": bruto,
        "bruto_mensual": bruto / pagas,
        "ss_empresa": ss,
        "coste_empresa": coste_empresa,
        "coste_total": coste_total,
        "dias_facturables": dias_facturables,
        "coste_dia": coste_dia,
        "tarifa_dia": tarifa_dia,
        "tarifa_hora": tarifa_dia / 8,
        "facturacion_anual": tarifa_dia * dias_facturables,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("bruto", type=float, help="salario bruto anual en EUR")
    p.add_argument("--margin", type=float, default=0.25, help="margen sobre venta (def. 0.25)")
    p.add_argument("--overhead", type=float, default=0.10, help="estructura/gastos generales sobre coste (def. 0.10)")
    p.add_argument("--utilization", type=float, default=0.85, help="ocupación sobre días laborables (def. 0.85)")
    p.add_argument("--work-days", type=float, default=225, help="días laborables/año sin festivos ni vacaciones (def. 225)")
    p.add_argument("--ss-rate", type=float, default=SS_EMPRESA, help="cotización empresa (def. 0.3215)")
    p.add_argument("--pagas", type=int, default=14, help="número de pagas (def. 14)")
    a = p.parse_args()

    r = calcular(a.bruto, a.margin, a.overhead, a.utilization, a.work_days, a.ss_rate, a.pagas)
    print(f"Bruto anual:            {r['bruto']:>10,.0f} € ({r['bruto_mensual']:,.0f} € x {a.pagas} pagas)")
    print(f"SS empresa:             {r['ss_empresa']:>10,.0f} €")
    print(f"Coste empresa:          {r['coste_empresa']:>10,.0f} €")
    print(f"Coste + overhead:       {r['coste_total']:>10,.0f} €")
    print(f"Días facturables:       {r['dias_facturables']:>10,.0f}")
    print(f"Coste por día:          {r['coste_dia']:>10,.0f} €")
    print(f"TARIFA DÍA:             {r['tarifa_dia']:>10,.0f} €")
    print(f"TARIFA HORA:            {r['tarifa_hora']:>10,.0f} €")
    print(f"Facturación anual:      {r['facturacion_anual']:>10,.0f} €")


if __name__ == "__main__":
    main()
