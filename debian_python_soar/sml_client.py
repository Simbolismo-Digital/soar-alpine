import Python_sml_ClientInterface as sml

# Cria o kernel e o agente
kernel = sml.Kernel.CreateKernelInCurrentThread(True, 0)
agent = kernel.CreateAgent("AgenteMinimo")

# Executa comando CLI simples
print(agent.ExecuteCommandLine("version").strip())

# Injeta dados no Input Link
input_link = agent.GetInputLink()
sensor = agent.CreateIdWME(input_link, "sensor")
agent.CreateStringWME(sensor, "tipo", "sentinel-2")
agent.CreateIntWME(sensor, "alerta_incendio", 1)

# Roda 1 ciclo
agent.RunSelf(1)

# Mostra memória de trabalho
print(agent.ExecuteCommandLine("print --depth 2 s1"))

# Finaliza
kernel.Shutdown()
