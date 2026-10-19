# Simulador de Lucros Reais

Calculadora pública de rendimentos reais mensais, executada **inteiramente no navegador**.

Site previsto: https://bollux78.github.io/simulador-lucros-reais/

## Recursos
- Patrimônio de R$ 0 a R$ 10 milhões, inicial 0.
- Renda externa líquida de R$ 0 a R$ 30 mil/mês, inicial 0.
- Rentabilidade de 10% a 200% do CDI.
- IR efetivo de 0% a 22,5%.
- CDI mensal (SGS 4391) e IPCA mensal (SGS 433) do Banco Central.
- Últimos 12 meses completos: tabela e gráfico.
- Atualização automática diária via GitHub Actions, com botão de execução manual na aba Actions.

## Privacidade
O site **não envia, armazena ou registra** os valores selecionados nos sliders. Não utiliza cookies próprios, analytics, localStorage, formulários ou backend. Apenas carrega HTML e JSON público do GitHub Pages. O provedor de hospedagem pode registrar metadados técnicos de acesso. Nenhum valor financeiro é incluído em URLs ou enviado ao GitHub.

## Segurança de edição
A leitura pública do repositório não concede permissão para edição. Somente usuários autorizados pelo proprietário podem fazer alterações. Recomenda-se ativar 2FA, revisar colaboradores e proteger a branch main nas configurações do repositório. O workflow possui permissão de escrita para atualizar somente o arquivo público de índices por commit, dentro das permissões do repositório.

## Ativar GitHub Pages
Em **Settings → Pages → Build and deployment → Source**, selecione **Deploy from a branch**. Em **Branch**, selecione **main**, pasta **/(root)**, e clique em **Save**.

Em **Settings → Actions → General → Workflow permissions**, selecione **Read and write permissions** para que a atualização automática possa publicar o JSON (caso a opção esteja disponível).

Em **Actions → Atualizar CDI e IPCA → Run workflow**, execute uma vez para gerar os dados iniciais. Caso a API do Banco Central esteja indisponível, o workflow falhará sem fabricar dados; tente novamente depois.

## Cálculo
CDI relativo no mês = (1 + CDI_mês)^percentual - 1.
Retorno líquido = CDI relativo × (1 − IR).
Lucro real = patrimônio × [(1 + retorno líquido)/(1 + IPCA_mês) − 1].
Renda total = lucro real + renda externa líquida.

Os valores representam uma simulação sobre patrimônio constante, não o extrato de uma carteira real.
