from abc import ABC, abstractmethod


class SistemaInventario:
    def verificar_stock(self, producto: str) -> bool:
        print(f"Verificando stock de {producto}...")
        return True


class SistemaEnvio:
    def organizar_envio(self, producto: str) -> None:
        print(f"Organizando el envio para {producto}...")


class InterfazPago(ABC):
    @abstractmethod
    def procesar_pago(self, cantidad: float) -> None:
        """Procesa el pago con la interfaz estandar de la tienda."""


class StripeLegacy:
    def charge_credit_card(self, total_dollars: float) -> None:
        print(f"[Stripe] Tarjeta cobrada por la cantidad de ${total_dollars}")


class StripeAdapter(InterfazPago):
    def __init__(self, stripe_legacy: StripeLegacy) -> None:
        self.stripe = stripe_legacy

    def procesar_pago(self, cantidad: float) -> None:
        self.stripe.charge_credit_card(cantidad)
        


class CompraFacade:
    def __init__(
        self,
        inventario: SistemaInventario,
        envio: SistemaEnvio,
        pago: InterfazPago,
    ) -> None:
        self.inventario = inventario
        self.envio = envio
        self.pago = pago

    def realizar_compra(self, producto: str, cantidad: float) -> None:
       if self.inventario.verificar_stock(producto):
           self.pago.procesar_pago(cantidad)
           self.envio.organizar_envio(producto)
           print("Compra realizada con éxito!")
       else:
             print("Lo sentimos, no hay stock del producto.")


def main() -> None:
    stripe_api = StripeLegacy()
    pago_adaptado = StripeAdapter(stripe_api)

    tienda = CompraFacade(
        inventario=SistemaInventario(),
        envio=SistemaEnvio(),
        pago=pago_adaptado,
    )

    tienda.realizar_compra("Laptop", 1200)


if __name__ == "__main__":
    main()

