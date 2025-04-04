
# Estrutura do Frontend

O frontend do sistema da CPA foi desenvolvido com **ReactJS**, priorizando **simplicidade**, **praticidade** e **usabilidade**. O foco é garantir que o usuário consiga interagir com o sistema de forma intuitiva, mesmo sem conhecimento avançado em tecnologia.

A escolha do **ReactJS** possibilita a criação de componentes reutilizáveis, facilitando a manutenção e a escalabilidade do projeto. O sistema é estruturado de forma modular, separando claramente as **páginas principais** e os **componentes de layout**.

## 📄 Páginas

-   **Home** – Página inicial do sistema.
    
-   **Importar** – Interface para envio de arquivos CSV ao sistema.
    
-   **Progresso** – Exibe o status do processamento dos arquivos.
    
-   **Gerar Relatório** – Permite a geração de relatórios a partir dos dados importados.
    
-   **Gerar PDF** – Gera e disponibiliza relatórios em formato PDF.
    

## 🏗️ Layout e Componentes

Para manter a organização visual e a consistência da interface, o sistema utiliza um layout base composto por:

-   **Container** – Estrutura geral que organiza o conteúdo das páginas.
    
-   **Header** – Cabeçalho com informações e navegação.
    
-   **NavBar** – Menu de navegação para facilitar o acesso às páginas.
    
-   **Footer** – Rodapé do sistema.
    
-   **PopupHeader** – Popup criado para verificação de Headers de csv.
    
-   **selectAutoWidth** – Um select com auto width.
    
-   **StyledInput** – Um input estilizado.
    
-   **uploadButton** – Botão para upload de arquivos.
    
-   **uploadButtonZip** – Botão para upload de arquivos zip.


Essa estrutura modular permite que o sistema seja facilmente expandido no futuro, mantendo a experiência do usuário fluida e acessível.