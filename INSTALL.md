# Como Habilitar o Login Root e Configurar a Tela TFT no Pwnagotchi
## 1. Habilitar o Login como Root
Siga os passos abaixo para liberar o login de root no sistema:

#### a. Defina uma nova senha para o root:

Abra o terminal e execute o seguinte comando:

```sudo passwd root```

Em seguida, digite e confirme a nova senha do root.

#### b. Edite o arquivo de configuração do SSH:

Abra o arquivo de configuração do SSH com o editor vim:


```vim /etc/ssh/sshd_config```

#### c. Modifique as permissões de login do root via SSH:

Comente a linha PermitRootLogin without-password, adicionando um # no início da linha:

```#PermitRootLogin without-password```

Logo abaixo, adicione a linha:

```PermitRootLogin yes```

#### d. Reinicie o serviço SSH:

```service ssh restart```

## 2. Configurar a Tela TFT 3.5 Polegadas

#### a. Configuração Inicial:

No arquivo config.toml, configure a tela para o modelo correto. Para a tela Spotpear 2.4", defina o parâmetro da seguinte forma:

```ui.display.type = "spotpear24inch"```

#### b. Editar o Arquivo Python da Tela:

Subistitua o arquivo spotpear24inch.py no diretório:

```/usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/hw/```

para ajustar as configurações da tela ao seu dispositivo.

[Tela](https://github.com/sposito88/pwnagotchi_3.5_TFT/tree/main/Tela)


#### c. Ativando a Tela com o Script LCD-show:

Para ativar a tela, execute o script LCD35-show da Waveshare. Os comandos a seguir irão clonar o repositório e ativar a tela:


```rm -rf LCD35-show && git clone https://github.com/waveshare/LCD-show.git```

```cd LCD-show/
chmod +x LCD35-show
./LCD35-show lite
