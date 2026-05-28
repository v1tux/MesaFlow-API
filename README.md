# MesaFlow

Sistema de gestão de pedidos, atendimento para restaurantes, bares e operações gastronômicas.

O **MesaFlow** nasceu com o objetivo de tornar o atendimento mais rápido, organizado e inteligente, conectando garçons, cozinha, bar e gestão em uma única experiência digital.

---

## Sobre o projeto

Em muitos restaurantes, o fluxo entre mesa, garçom, cozinha, bar e caixa ainda depende de comunicação manual, anotações soltas ou sistemas pouco intuitivos.

O MesaFlow propõe uma solução moderna para esse problema: um sistema onde o garçom pode lançar pedidos diretamente pela aplicação, acompanhar o status de preparo, organizar mesas, adicionar observações importantes e melhorar a comunicação entre todos os setores da operação.

A ideia é reduzir erros, agilizar o atendimento e oferecer ao gestor mais controle sobre o funcionamento do restaurante.

---

## Principais funcionalidades

- Cadastro e gerenciamento de mesas
- Inclusão de clientes ou pessoas por mesa
- Visualização de pratos com imagem, nome, descrição e preço
- Envio automático dos pedidos para cozinha ou bar
- Status de preparo dos itens
- Notificação quando um item estiver pronto
- Observações por pedido, como alergias ou preferências
- Controle de tempo médio de preparo
- Organização por setores: salão, cozinha, bar e caixa
- Visualização de ticket médio
- Histórico de pedidos por mesa
- Fluxo pensado para uso em celular, tablet ou desktop

---

## Problema que o MesaFlow resolve

Restaurantes costumam lidar com desafios como:

- Pedidos anotados de forma incorreta
- Comunicação lenta entre salão e cozinha
- Falta de visibilidade sobre o andamento dos pratos
- Dificuldade para controlar mesas ocupadas
- Erros em observações importantes, como alergias
- Falta de dados para tomada de decisão
- Tempo de atendimento acima do ideal

O MesaFlow busca centralizar esse processo e transformar o atendimento em um fluxo mais claro, rastreável e eficiente.

---

## Diferenciais do projeto

- Interface simples para uso rápido durante o atendimento
- Foco em experiência real de restaurante
- Organização por categorias de produtos
- Pensado para expansão futura como SaaS
- Possibilidade de integração com cozinha, bar, estoque e pagamentos
- Estrutura preparada para evoluir com permissões, relatórios e dashboards
- Produto inspirado em problemas reais de operação gastronômica

---

## Fluxo principal

1. O garçom seleciona a mesa.
2. Adiciona clientes ou quantidade de pessoas.
3. Escolhe os produtos do cardápio.
4. Insere observações, se necessário.
5. Envia o pedido.
6. A cozinha ou o bar recebe o item.
7. O responsável atualiza o status.
8. O garçom é notificado quando estiver pronto.
9. O pedido é entregue e fica registrado no histórico da mesa.

---

## Exemplo de pedido

```json
{
  "mesa": 8,
  "cliente": "Mesa 8",
  "itens": [
    {
      "produto": "Risoto de Camarão",
      "quantidade": 1,
      "observacao": "Cliente alérgico a camarão. Retirar camarão do preparo."
    }
  ],
  "status": "em_preparo"
}