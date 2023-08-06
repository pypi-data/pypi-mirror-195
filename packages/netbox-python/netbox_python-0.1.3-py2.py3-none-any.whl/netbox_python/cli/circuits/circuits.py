import typer

from . import circuit_terminations

# self.circuit_terminations = self._circuit_terminations(client)
# self.circuit_types = self._circuit_types(client)
# self.circuits = self._circuits(client)
# self.provider_networks = self._provider_networks(client)
# self.providers = self._providers(client)


app = typer.Typer()
app.add_typer(circuit_terminations.app, name="circuit_terminations")
