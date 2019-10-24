############################
# default_analytic_account #
###########################

Este módulo permite cargar por defecto el Centro de Costo (cuenta analíitica) al crear Pedidos y Facturas de Compra o Venta.

Caracteristicas Generales:
=========================

- Adiciona el campo "Cuenta Analítica" en la ficha del Producto y del Partner.
- Toma como principal criterio de busqueda la cuenta analítica asociada al Producto, luego la del Partner.
- En el caso de Pedidos de Venta, busca principalmente la cuenta analítica asociada al pedido directamente(Funcionamiento Original) y luego el criterio antes mencionado.


Configuraciones Generales:
=========================
- Este módulo instala los modulos de Compra, Venta, Contabilidad y Cuentas Analíticas.

Acerca de permísologia:
======================
- Se deben activar los permisos de "Cuenta Analitica" para compra y venta en el perfil del usuario.
