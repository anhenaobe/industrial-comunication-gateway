# Estado del proyecto — Gateway académico Rev1

Actualización: 2026-11-09. **NO-GO para transferencia a PCB** hasta reparar y verificar los modelos en Altium. No se ejecutó ECO ni se modificó PCB1.PcbDoc.

## Evidencia y fases

- Fase 1 cerrada en dc890fe según estado heredado: CHASSIS separado de GND, conectores de buses, R34 de 1 MΩ y cabeceras de depuración. C65 permanece en 1 nF/2 kV 1206 por decisión del usuario.
- Fase 2 revisada en la sesión anterior: alcance jerárquico, Power en TopLevel (HTGYNFPM), alimentación global, anotación completa; ERC comunicado: cero errores sin suprimir y cuatro errores intencionales suprimidos (U1.4, U5.1/26/27). No se repitió ERC en esta sesión.
- Fase 3 sigue abierta y sin commit de los archivos CAD: cambios heredados de footprints y decoración en PcbLib, pendientes de verificación nativa.
- Auditoría offline de los archivos guardados: 134 componentes, ningún modelo con nombre GW_CAND_*. El JSON adjunto conserva parámetros, UID, modelos, propietarios y comparación contra HEAD. No sustituye obj_query ni compilación.
- Backend EDA de Electronics AI detenido durante inicialización: transport_closed, diagnóstico 62e28f9c2de84b9fbb1104ec28fcde58. Doctor fuera del sandbox: configured/ready=true, sin incidencias; no comprueba el editor. La conexión de esta sesión no ofrece reinicio. Es necesario reconectar el plugin para completar la verificación.

## Fixes heredados

| Hoja | Componente/pin | Antes | Después comunicado |
|---|---|---|---|
| Ethernet | J2.S1/S2, C46.1, C52.1, R34.2, C65.2 | Blindaje flotante/retorno GND | CHASSIS, seis pines, separado de GND |
| Ethernet | R34 | Valor anterior | RC0603FR-071ML, 1 MΩ |
| Field_IO | J9 | Bus sin borne | 1=A, 2=B, 3=GND; D4 SM712 |
| Field_IO | J10 | Bus sin borne | 1=CANH, 2=CANL, 3=GND |
| MCU | J8 | Cabecera pendiente | 1=BOOT0, 2=3.3V |
| Power | U1 EP | Pads 11A–11D | Modelo EPU con pads llamados 11; pendiente verificar nativamente |

## Bloqueo de modelos confirmado offline

26 RECORD 45 tienen propietario distinto de RECORD 44, en 24 componentes. No se modificaron los SchDoc en esta sesión: no se puede cerrar/reabrir y verificar el proyecto con el backend detenido.

| Hoja | Componentes con modelo huérfano |
|---|---|
| Power | D1, U1, C2, C1, R1, R3, R4, R2, C17, C60, C16, C61, C7, C12, C21 |
| Ethernet | R12, R14, C46, R19, R17, C52, C65 |
| Field_IO | R22, R21 |

C1/C2 tienen dos modelos current cada uno. U2/U3 tienen un modelo current y una alternativa inactiva; no eliminar la alternativa por confundirla con un duplicado. Los 33 warnings heredados no equivalen al número de huérfanos; siguen pendientes de recompilación.

## Footprints modificados respecto a dc890fe

Comparación offline de nombres de modelos guardados; fuente indicada por los parámetros CAD de la instancia. No certifica dimensiones ni disponibilidad en Altium.

| Hoja / designador | Viejo | Nuevo guardado | Fuente de la instancia |
|---|---|---|---|
| Power / L1 |  | GW_XAL4030_COILCRAFT | Professor_shared.SchLib glyph Inductor_10uH_4A_7.2*6.6mm |
| Power / C6 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C4 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C5 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / R6 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Power / C8 | GW_CAND_0805_cap | GW_0805_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| Power / C9 | GW_CAND_0805_cap | GW_0805_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| Power / C11 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C10 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / R7 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Power / J1 | CUI_TB002-500-02BE | GW_TB002_500_2P_SAMESKY | Biblioteca local; verificación pendiente |
| Power / L2 |  | GW_XAL4040_COILCRAFT | Professor_shared.SchLib glyph Inductor_10uH_4A_7.2*6.6mm |
| Power / C15 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C13 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C14 |  | GW_C3225_TDK_REFLOW | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / R9 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Power / C18 | GW_CAND_0805_cap | GW_0805_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| Power / C20 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / C19 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / R10 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Power / F1 |  | GW_0451_LITTELFUSE | Official451/453 series Rev01-Dec-2025 pp1-4; electrical row002 and ordering |
| Power / U1 | GW_DRC0010J_TI_TPS2662 | GW_DRC0010J_TI_TPS2662_EPU | TI TPS2662 SLVSDT4F Dec2021 Table6-1 p4; DRC0010J4218878/B board p44/stencil p45 |
| Power / C3 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Power / R5 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Power / R8 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| MCU / C22 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C31 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C32 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C26 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C35 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C27 | GW_CAND_0805_cap | GW_0805_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| MCU / C33 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C34 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C30 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C29 | GW_CAND_0603_cap | GW_SAMSUNG_CL10_1608_REFLOW | Professor_shared.SchLib glyph Cap_1uF_0603_50V |
| MCU / C24 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / C23 | GW_CAND_0603_cap | GW_SAMSUNG_CL10_1608_REFLOW | Professor_shared.SchLib glyph Cap_1uF_0603_50V |
| MCU / C28 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / R11 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| MCU / C25 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / J3 | GW_CAND_H_6x1_TH_100mil | GW_WRPHD_6X1_254_WURTH | schematic_construction_guide.md line 410, manufacturer PDF not in repo, IPC-7351 generic 2.54 mm land used |
| MCU / C62 | GW_CAND_0603_cap | GW_SAMSUNG_CL10_1608_REFLOW | Professor_shared.SchLib glyph Cap_1uF_0603_50V |
| MCU / C63 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| MCU / J8 | GW_CAND_H_2x1_TH_100mil | GW_WRPHD_2X1_254_WURTH | schematic_construction_guide.md line 410, manufacturer PDF not in repo, IPC-7351 generic 2.54 mm land used |
| Ethernet / R13 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Ethernet / C37 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C38 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C39 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C40 | GW_CAND_0603_cap | GW_SAMSUNG_CL10_1608_REFLOW | Professor_shared.SchLib glyph Cap_1uF_0603_50V |
| Ethernet / C41 | GW_CAND_0805_cap | GW_SAMSUNG_CL21_2012_REFLOW | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| Ethernet / R15 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Ethernet / C36 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C47 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C48 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C49 | GW_CAND_0603_cap | GW_SAMSUNG_CL10_1608_REFLOW | Professor_shared.SchLib glyph Cap_1uF_0603_50V |
| Ethernet / C50 | GW_CAND_0805_cap | GW_SAMSUNG_CL21_2012_REFLOW | Professor_shared.SchLib glyph Cap_10uF_0805_25V_ |
| Ethernet / C43 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C42 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C45 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C44 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / R16 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Ethernet / R18 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Ethernet / C51 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C53 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Ethernet / C54 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Field_IO / C56 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Field_IO / R23 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Field_IO / C57 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Field_IO / R20 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Field_IO / C55 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Field_IO / R24 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Field_IO / C59 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |
| Field_IO / R30 | GW_CAND_0603_res | GW_RC0603_YAGEO_REFLOW | Professor_shared.SchLib glyph Res_10k_0603_1/10W |
| Field_IO / C58 | GW_CAND_0603_cap | GW_0603_KEMET_NOMINAL | Professor_shared.SchLib glyph Cap_0.1uF_0603_50V |

## Temas escalados: requieren decisión del usuario

- Mantener FOJAN FRC0603J103TS o sustituir MPN por Yageo RC0603FR-0710KL: afecta al BOM. El land 0603 asignado no cambia el MPN.
- CIN de buck: tres C5750 de 4,7 µF frente a cinco previstos; confirmar capacidad efectiva bajo polarización. Salida: cuatro de 15 µF por riel frente a tres en TI Table 10-1.
- R36: CRCW 1206 frente al 0603 solicitado, Not Fitted; confirmar aceptación.
- TDS3311: archivo local HTML, falta PDF auténtico. Alturas TB002 y SS3P6L aproximadas: validar antes de revisión mecánica.
- Discrepancia de variante: el archivo guardado tiene ocho Not Fitted (C11, C20, R6, R9, R34, C65, R35, R36); C2 no figura. El estado heredado indica C2 Not Fitted. Resolver en Altium y guardar sin perder los UID.

## Pendientes para cerrar fase 3

1. Reconectar Electronics AI y comprobar app_context contra el proyecto explícito.
2. Cerrar documentos antes de reparar copias del FileHeader; conservar respaldo, hijos 46/47/48, todos los OWNERINDEX, geometría, parámetros y UID. Eliminar solo los duplicados de C1/C2. Alternativa: recolocar desde SchLib conservando metadatos y variante.
3. Reabrir y forzar compilación: cero Missing component models; obj_query eSchComponent.Models con exactamente un modelo current por instancia. Verificar resolución de todos los footprints y EP de U1.
4. Resolver discrepancia C2, revisar alturas, courtyard y serigrafía; revisar el paquete RNX entregado para U2/U3.
5. Guardar y hacer commit de fase 3 con PcbLib, SchLib, SchDocs y PrjPcb; push normal a origin/main. No ejecutar ECO.

Auditoría detallada: [model_audit_rev1.json](evidence/model_audit_rev1.json).
