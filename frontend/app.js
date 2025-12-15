document.addEventListener('DOMContentLoaded', () => {
    // --- Elementos do DOM ---
    const proposalForm = document.getElementById('proposal-form');
    const generateBtn = document.getElementById('generate-btn');
    const loading = document.getElementById('loading');
    const resultText = document.getElementById('result-text');
    const historyList = document.getElementById('history-list');
    
    const addProblemBtn = document.getElementById('add-problem-btn');
    const problemsContainer = document.getElementById('problems');
    let problemCount = 0;

    const mediaUrlInput = document.getElementById('media-url');
    const mediaFileInput = document.getElementById('media-file');

    const addTemplateBtn = document.getElementById('add-template-btn');
    const viewTemplatesBtn = document.getElementById('view-templates-btn');
    const templateModal = document.getElementById('template-modal');
    const viewTemplatesModal = document.getElementById('view-templates-modal');
    
    // --- Lógica de Problemas ---
    addProblemBtn.addEventListener('click', () => {
        problemCount++;
        const newProblemDiv = document.createElement('div');
        newProblemDiv.classList.add('problem-item');
        newProblemDiv.innerHTML = `
            <input type="text" id="problem-${problemCount}" placeholder="Descreva o problema ${problemCount}">
            <button type="button" class="remove-problem-btn">&times;</button>
        `;
        problemsContainer.appendChild(newProblemDiv);

        newProblemDiv.querySelector('.remove-problem-btn').addEventListener('click', (e) => {
            e.target.closest('.problem-item').remove();
        });
    });

    // --- Submissão do Formulário ---
    proposalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loading.style.display = 'block';
        resultText.textContent = '';
        
        const formData = new FormData();
        
        formData.append('nome', document.getElementById('nome').value);
        formData.append('empresa', document.getElementById('empresa').value);
        formData.append('nicho', document.getElementById('nicho').value);
        formData.append('onde', document.getElementById('onde').value);
        formData.append('ponto', document.getElementById('ponto').value);
        
        const problems = Array.from(document.querySelectorAll('.problem-item input'))
                              .map(input => input.value)
                              .filter(value => value);
        formData.append('problems', JSON.stringify(problems));

        // Temporarily disable media uploads to fix core issue
        // if (mediaUrlInput.value) {
        //     formData.append('media_url', mediaUrlInput.value);
        // }
        // for (const file of mediaFileInput.files) {
        //     formData.append('media_files', file);
        // }

        try {
            const response = await fetch('/generate-proposal', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Erro no servidor');
            }

            const result = await response.json();
            resultText.textContent = result.proposal;
            addToHistory(result.proposal);

        } catch (error) {
            resultText.textContent = `Erro: ${error.message}`;
        } finally {
            loading.style.display = 'none';
        }
    });

    // --- Lógica de Templates ---
    addTemplateBtn.addEventListener('click', () => openModal(templateModal));
    viewTemplatesBtn.addEventListener('click', async () => {
        await loadTemplates();
        openModal(viewTemplatesModal);
    });

    document.getElementById('save-template-btn').addEventListener('click', async () => {
        const name = document.getElementById('new-template-name').value;
        const content = document.getElementById('new-template-content').value;
        const instructions = document.getElementById('new-template-instructions').value;

        if (!name || !content) {
            alert('Nome e conteúdo do template são obrigatórios.');
            return;
        }

        try {
            const response = await fetch('/templates/human', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, content, instructions, type: 'human' }),
            });
            if (!response.ok) throw new Error('Falha ao salvar template.');
            alert('Template salvo com sucesso!');
            closeModal(templateModal);
        } catch (error) {
            alert(error.message);
        }
    });

    async function loadTemplates() {
        try {
            const response = await fetch('/templates');
            if (!response.ok) throw new Error('Falha ao carregar templates.');
            const templates = await response.json();
            
            const lists = {
                'human-adm': document.getElementById('human-adm-templates-list'),
                'human': document.getElementById('human-templates-list'),
                'ai': document.getElementById('ai-templates-list'),
            };

            Object.values(lists).forEach(list => list.innerHTML = '');

            (templates.human_adm || []).forEach(t => lists['human-adm'].appendChild(createTemplateItem(t)));
            (templates.human || []).forEach(t => lists['human'].appendChild(createTemplateItem(t)));
            (templates.ai || []).forEach(t => lists['ai'].appendChild(createTemplateItem(t)));
            
            // Ativa a primeira aba por padrão após carregar
            const firstTab = document.querySelector('#view-templates-modal .tablinks');
            if (firstTab) {
                openTab(firstTab.dataset.tab);
            }

        } catch (error) {
            console.error(error);
        }
    }
    
    function createTemplateItem(template) {
        const li = document.createElement('li');
        // O nome do template é o nome do arquivo .json
        li.textContent = template.name || 'Template sem nome';
        li.addEventListener('click', () => {
            // Abre o relatório do template em uma nova aba
            window.open(`/templates/report/${template.filename}`, '_blank');
            closeModal(viewTemplatesModal);
        });
        return li;
    }

    // --- Lógica de Histórico ---
    function addToHistory(text) {
        const li = document.createElement('li');
        const preview = text.length > 80 ? text.substring(0, 80) + '...' : text;
        li.textContent = preview;
        li.dataset.fullText = text;
        
        li.addEventListener('click', () => {
            resultText.textContent = li.dataset.fullText;
        });
        
        historyList.prepend(li);
    }

    // --- Funções de Modal ---
    function openModal(modal) {
        modal.style.display = 'block';
    }

    function closeModal(modal) {
        modal.style.display = 'none';
    }

    document.querySelectorAll('.modal .close-button').forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal')));
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target);
        }
    });
    
    // --- Lógica de Abas ---
    const tabContainer = document.querySelector('#view-templates-modal .tab');

    function openTab(tabId) {
        const tabContents = document.querySelectorAll('#view-templates-modal .tabcontent');
        const tabs = document.querySelectorAll('#view-templates-modal .tablinks');

        tabs.forEach(tab => tab.classList.remove('active'));
        document.querySelector(`[data-tab='${tabId}']`).classList.add('active');

        tabContents.forEach(content => content.classList.remove('active'));
        const activeContent = document.getElementById(tabId);
        if (activeContent) {
            activeContent.classList.add('active');
        }
    }

    if (tabContainer) {
        tabContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('tablinks')) {
                const tabId = e.target.dataset.tab;
                openTab(tabId);
            }
        });
    }
});