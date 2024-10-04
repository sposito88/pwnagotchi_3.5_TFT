# pwnagotchi_3.5_TFT
"Plugin e arquivos de configuração para otimizar o Pwnagotchi em uma tela TFT de 3,5 polegadas, incluindo ajustes na interface e melhorias no rastreamento de experiência (EXP). A imagem utilizada é baseada na versão v1.5.5 do Pwnagotchi, disponível em https://github.com/evilsocket/pwnagotchi/releases/tag/v1.5.5."


Suporte à Localização com Arquivos .po e .mo
O projeto já inclui suporte à localização (i18n) utilizando arquivos .po e .mo. Isso permite que o Pwnagotchi exiba textos e mensagens em diferentes idiomas, incluindo português do Brasil.

Caminho dos Arquivos de Localização:
Os arquivos de localização já estão disponíveis no seguinte caminho:
/usr/local/src/pwnagotchi/pwnagotchi/locale/pt-BR/LC_MESSAGES/

Como Funciona:
O arquivo .mo já está incluído no caminho correto, e o Pwnagotchi irá carregá-lo automaticamente ao detectar o idioma do sistema.
O arquivo .po foi utilizado para gerar o arquivo .mo que contém as traduções de todas as mensagens da interface.
Adicionando Novos Idiomas:
Caso você queira adicionar suporte para outros idiomas, basta seguir os passos abaixo:

Interface em Múltiplos Idiomas: O Pwnagotchi poderá ser utilizado em diferentes idiomas de acordo com as preferências do usuário.
Adição Fácil de Novos Idiomas: Novos idiomas podem ser adicionados rapidamente com o uso dos arquivos .po e .mo.


Alterações no Age Plugin
O Age Plugin foi atualizado para melhorar a exibição da idade do Pwnagotchi e fornecer mais opções de controle de log para depuração.

Alterações principais:
Exibição de idade mínima: Agora, se a idade do Pwnagotchi for negativa ou menor que zero, o código exibe a mensagem "Começando a explorar!".
Caso o Pwnagotchi tenha menos de um dia de idade, o código exibe "Começando a explorar!", garantindo que algo significativo seja mostrado na tela.

Antes: A idade ficava vazia se o Pwnagotchi tivesse menos de 1 dia ou uma idade negativa.
Agora: Para idades abaixo de zero, a mensagem exibida é "Começando a explorar!", e a idade mínima exibida é "Começando a explorar!" para Pwnagotchi recém-criados.
Depuração reforçada: Continuamos com logs detalhados para verificar se o cálculo de idade está sendo processado corretamente. Os valores são verificados e
passados para a interface de usuário (UI) sem problemas, permitindo uma análise mais eficiente caso algo não funcione como esperado.

Comportamento esperado:
Agora, mesmo que o Pwnagotchi tenha acabado de "nascer" e tenha poucos minutos de idade, o valor exibido será "Hoje" ou "0d". Se a idade for negativa,
a mensagem "Começando a explorar!" será exibida, garantindo que a interface sempre mostre uma informação adequada.
Controle de Logs:
Adicionamos um sistema de logging que permite ativar ou desativar os logs conforme a necessidade de depuração. Isso foi feito através das seguintes modificações:

Variável de controle ENABLE_LOGGING: Esta variável controla a ativação dos logs. Por padrão, está definida como False (logs desativados), mas pode ser alterada para True para ativar a saída de logs.

Para ativar os logs: Defina ENABLE_LOGGING = True.
Para desativar os logs (padrão): Mantenha ENABLE_LOGGING = False.
Função log(): Criamos uma função que centraliza o controle de logs. Se ENABLE_LOGGING estiver ativado, a função log() exibirá as mensagens apropriadas no console,
permitindo a depuração sem a necessidade de alterar o código em múltiplos pontos.

Exemplo de Uso:
Ativando logs:

ENABLE_LOGGING = True
Desativando logs:

ENABLE_LOGGING = False  # Padrão
Essa abordagem facilita a ativação e desativação de logs, proporcionando maior controle sobre o comportamento do código sem comprometer a eficiência do sistema.

Com essas melhorias, o Age Plugin agora é mais robusto, exibe informações claras mesmo em situações de idade mínima ou negativa, e oferece maior flexibilidade para depuração quando necessário.

