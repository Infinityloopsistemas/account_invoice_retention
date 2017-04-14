.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3


Account Invoice Retention Guarantee
===================================

Este modulo implementa en facturación la opción de poder retener las garantías en el sector construcción.

Estas retenciones se practican sobre facturaciones en el ramo de la construcción ,son para garantizar la calidad de la obra
Existen 2 escenarios el DE OBRA FINALIZADA  y en CURSO por lo que en el primero la retención se resta del total de la factura
la base imponible y a posterior se calcula el impuesto


Configuración
_____________

Se definien los diferentes tipos de retenciones por garantias en apartado Retenciones en Contabilidad->Configuración.
Dependiendo si es para OBRA FINALIZADA o en EN CURSO, existe 2 opciones (ANTES Y DESPUES) ya que lo que determina el calculo del impuesto.


Funcionalidades
______________

+ Multiples retenciones a diferentes tipos de porcentaje
+ Genera el asienteo de retención una vez validada la factura.
+ Genera factura indicando la retención y el importe total de factura.