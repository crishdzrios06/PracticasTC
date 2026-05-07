from graphviz import Digraph
import os


class RenderizadorAutomata:

    @staticmethod
    def generar_afd(estados, inicial, finales, transiciones):

        dot = Digraph(format="png")

        dot.attr(rankdir="LR")

        for estado in estados:

            if estado in finales:
                dot.node(
                    estado,
                    shape="doublecircle"
                )
            else:
                dot.node(
                    estado,
                    shape="circle"
                )

        dot.node("", shape="none")
        dot.edge("", inicial)

        for (origen, simbolo), destino in transiciones.items():

            if isinstance(destino, list):

                for d in destino:

                    dot.edge(
                        origen,
                        d,
                        label=simbolo
                    )

            else:

                dot.edge(
                    origen,
                    destino,
                    label=simbolo
                )

        if not os.path.exists("assets"):
            os.makedirs("assets")

        ruta = "assets/automata"

        dot.render(ruta, cleanup=True)

        return ruta + ".png"