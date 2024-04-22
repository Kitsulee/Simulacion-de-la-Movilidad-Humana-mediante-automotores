import sys
sys.path.append('../AI-Simulation')
from pln.reporter import *

text=[]
text.append("Evento occurrido a las 1 horas.Habian 10 personas en la parada de buses de Plaza de la Revolucion.Habian 10 personas en la parada de buses de Playa.Habian 10 personas en la parada de buses de La Habana Vieja.Habian 10 personas en la parada de buses de Centro Habana.Habian 10 personas en la parada de buses de Cerro.Habian 0 personas en el bus P1.Habian 0 personas en el bus P2.Habian 0 personas en el bus P3.Habian 0 personas en el bus P4.")
text.append("Evento occurrido a las 2 horas.Habian 8 personas en la parada de buses de Plaza de la Revolucion.Habian 12 personas en la parada de buses de Playa.Habian 10 personas en la parada de buses de La Habana Vieja.Habian 4 personas en la parada de buses de Centro Habana.Habian 6 personas en la parada de buses de Cerro.Habian 3 personas en el bus P1.Habian 7 personas en el bus P2.Habian 0 personas en el bus P3.Habian 0 personas en el bus P4.")
text.append("Evento occurrido a las 3 horas.Habian 6 personas en la parada de buses de Plaza de la Revolucion.Habian 14 personas en la parada de buses de Playa.Habian 10 personas en la parada de buses de La Habana Vieja.Habian 6 personas en la parada de buses de Centro Habana.Habian 6 personas en la parada de buses de Cerro.Habian 0 personas en el bus P1.Habian 5 personas en el bus P2.Habian 5 personas en el bus P3.Habian 8 personas en el bus P4.")
text.append("Evento occurrido a las 4 horas.Habian 4 personas en la parada de buses de Plaza de la Revolucion.Habian 16 personas en la parada de buses de Playa.Habian 10 personas en la parada de buses de La Habana Vieja.Habian 8 personas en la parada de buses de Centro Habana.Habian 8 personas en la parada de buses de Cerro.Habian 0 personas en el bus P1.Habian 0 personas en el bus P2.Habian 0 personas en el bus P3.Habian 0 personas en el bus P4.")


reporter = Reporter(text)
reporter.report()
