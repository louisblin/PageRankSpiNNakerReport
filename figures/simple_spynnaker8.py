import spynnaker8 as sim
import pyNN.utility.plotting as plot
import matplotlib.pyplot as plt


# Setup SpiNNaker with for 1 microsec time steps
sim.setup(timestep=1.0)

# Define a population of 1 neuron that will spike once at time t=0
pIn = sim.Population(1, sim.SpikeSourceArray(spike_times=[0]), label="input")
# Define a population of 1 neuron with neuron model `IF_curr_exp'
pOut = sim.Population(1, sim.IF_curr_exp(), label="output")
# Define a synapse link pIn -> pOut with synapse model `StaticSynapse'
sim.Projection(pIn, pOut, sim.OneToOneConnector(),
                     synapse_type=sim.StaticSynapse(weight=5, delay=1))

# Set spikes and voltage to be recorded at each time step
pOut.record(["spikes", "v"])

# Starts the simulation
simtime = 10  # ms
sim.run(simtime)

# Collect recorded data
neo = pOut.get_data(variables=["spikes", "v"])
spikes = neo.segments[0].spiketrains
v = neo.segments[0].filter(name='v')[0]
sim.end()

# Display graphs
plot.Figure(
    # plot voltage for first ([0]) neuron
    plot.Panel(v, ylabel="Membrane potential (mV)", data_labels=[pOut.label],
               yticks=True, xlim=(0, simtime)),
    # plot spikes (or in this case spike)
    plot.Panel(spikes, yticks=True, markersize=5, xlim=(0, simtime)),
    title="Simple Example",
    annotations="Simulated with {}".format(sim.name())
)
plt.show()
