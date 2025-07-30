// Moroccan Hospitals Management System - Frontend JavaScript
class HospitalManager {
    constructor() {
        this.currentHospitals = [];
        this.currentPage = 1;
        this.itemsPerPage = 10;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadHospitals();
        this.loadStatistics();
    }

    // Event Bindings
    bindEvents() {
        // Search functionality
        document.getElementById('searchBtn')?.addEventListener('click', () => this.searchHospitals());
        document.getElementById('clearSearchBtn')?.addEventListener('click', () => this.clearSearch());
        
        // CRUD operations
        document.getElementById('addHospitalBtn')?.addEventListener('click', () => this.showCreateModal());
        document.getElementById('saveHospitalBtn')?.addEventListener('click', () => this.saveHospital());
        document.getElementById('confirmDeleteBtn')?.addEventListener('click', () => this.confirmDelete());
        
        // Data management
        document.getElementById('loadDataBtn')?.addEventListener('click', () => this.loadDataFile());
        document.getElementById('createSampleBtn')?.addEventListener('click', () => this.createSampleData());
        document.getElementById('exportDataBtn')?.addEventListener('click', () => this.exportData());
        
        // File upload
        document.getElementById('jsonFileInput')?.addEventListener('change', (e) => this.handleFileUpload(e));
        
        // Modal close events
        document.querySelectorAll('[data-bs-dismiss="modal"]').forEach(btn => {
            btn.addEventListener('click', () => this.closeModals());
        });

        // Search on Enter key
        document.querySelectorAll('.search-input').forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.searchHospitals();
                }
            });
        });

        // Pagination
        document.getElementById('prevPageBtn')?.addEventListener('click', () => this.previousPage());
        document.getElementById('nextPageBtn')?.addEventListener('click', () => this.nextPage());
    }

    // API Methods
    async makeRequest(url, options = {}) {
        try {
            const response = await fetch(url, {
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                ...options
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error('API Request failed:', error);
            this.showAlert('Error: ' + error.message, 'danger');
            throw error;
        }
    }

    // Load and Display Hospitals
    async loadHospitals() {
        try {
            this.showLoading(true);
            const hospitals = await this.makeRequest('/api/hospitals');
            this.currentHospitals = hospitals;
            this.renderHospitalsTable();
            this.renderPagination();
        } catch (error) {
            console.error('Failed to load hospitals:', error);
        } finally {
            this.showLoading(false);
        }
    }

    renderHospitalsTable() {
        const tableBody = document.getElementById('hospitalsTableBody');
        if (!tableBody) return;

        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const hospitalsToShow = this.currentHospitals.slice(startIndex, endIndex);

        if (hospitalsToShow.length === 0) {
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="bi bi-inbox fs-1 text-muted"></i>
                        <p class="text-muted mt-2">Aucun hôpital trouvé</p>
                    </td>
                </tr>
            `;
            return;
        }

        tableBody.innerHTML = hospitalsToShow.map(hospital => `
            <tr>
                <td><strong>${hospital._id || hospital.id || 'N/A'}</strong></td>
                <td>${hospital.nom_etablissement || 'N/A'}</td>
                <td><span class="badge bg-primary">${hospital.region || 'N/A'}</span></td>
                <td>${hospital.delegation || 'N/A'}</td>
                <td>${hospital.commune || 'N/A'}</td>
                <td><span class="badge bg-secondary">${hospital.categorie || 'N/A'}</span></td>
                <td>
                    <div class="btn-group" role="group">
                        <button class="btn btn-sm btn-outline-info" onclick="hospitalManager.viewHospital('${hospital._id || hospital.id}')" title="Voir">
                            <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-warning" onclick="hospitalManager.editHospital('${hospital._id || hospital.id}')" title="Modifier">
                            <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" onclick="hospitalManager.deleteHospital('${hospital._id || hospital.id}')" title="Supprimer">
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    renderPagination() {
        const totalPages = Math.ceil(this.currentHospitals.length / this.itemsPerPage);
        const paginationInfo = document.getElementById('paginationInfo');
        const prevBtn = document.getElementById('prevPageBtn');
        const nextBtn = document.getElementById('nextPageBtn');

        if (paginationInfo) {
            const startItem = (this.currentPage - 1) * this.itemsPerPage + 1;
            const endItem = Math.min(this.currentPage * this.itemsPerPage, this.currentHospitals.length);
            paginationInfo.textContent = `${startItem}-${endItem} sur ${this.currentHospitals.length}`;
        }

        if (prevBtn) prevBtn.disabled = this.currentPage <= 1;
        if (nextBtn) nextBtn.disabled = this.currentPage >= totalPages;
    }

    previousPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            this.renderHospitalsTable();
            this.renderPagination();
        }
    }

    nextPage() {
        const totalPages = Math.ceil(this.currentHospitals.length / this.itemsPerPage);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            this.renderHospitalsTable();
            this.renderPagination();
        }
    }

    // Search Functionality
    async searchHospitals() {
        const searchParams = {
            region: document.getElementById('searchRegion')?.value || '',
            delegation: document.getElementById('searchDelegation')?.value || '',
            commune: document.getElementById('searchCommune')?.value || '',
            categorie: document.getElementById('searchCategorie')?.value || '',
            nom_etablissement: document.getElementById('searchNom')?.value || ''
        };

        try {
            this.showLoading(true);
            const params = new URLSearchParams(searchParams);
            const results = await this.makeRequest(`/api/search?${params}`);
            this.currentHospitals = results;
            this.currentPage = 1;
            this.renderHospitalsTable();
            this.renderPagination();
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            this.showLoading(false);
        }
    }

    clearSearch() {
        document.querySelectorAll('.search-input').forEach(input => input.value = '');
        this.loadHospitals();
    }

    // CRUD Operations
    showCreateModal() {
        this.resetForm();
        document.getElementById('hospitalModalTitle').textContent = 'Ajouter un Hôpital';
        document.getElementById('hospitalId').value = '';
        const modal = new bootstrap.Modal(document.getElementById('hospitalModal'));
        modal.show();
    }

    async viewHospital(hospitalId) {
        try {
            const hospital = await this.makeRequest(`/api/hospitals/${hospitalId}`);
            this.populateForm(hospital);
            document.getElementById('hospitalModalTitle').textContent = 'Détails de l\'Hôpital';
            
            // Make form read-only
            document.querySelectorAll('#hospitalForm input, #hospitalForm select').forEach(el => {
                el.setAttribute('readonly', true);
                el.setAttribute('disabled', true);
            });
            
            document.getElementById('saveHospitalBtn').style.display = 'none';
            const modal = new bootstrap.Modal(document.getElementById('hospitalModal'));
            modal.show();
        } catch (error) {
            console.error('Failed to load hospital details:', error);
        }
    }

    async editHospital(hospitalId) {
        try {
            const hospital = await this.makeRequest(`/api/hospitals/${hospitalId}`);
            this.populateForm(hospital);
            document.getElementById('hospitalModalTitle').textContent = 'Modifier l\'Hôpital';
            document.getElementById('hospitalId').value = hospitalId;
            
            // Make form editable
            document.querySelectorAll('#hospitalForm input, #hospitalForm select').forEach(el => {
                el.removeAttribute('readonly');
                el.removeAttribute('disabled');
            });
            
            document.getElementById('saveHospitalBtn').style.display = 'block';
            const modal = new bootstrap.Modal(document.getElementById('hospitalModal'));
            modal.show();
        } catch (error) {
            console.error('Failed to load hospital for editing:', error);
        }
    }

    async saveHospital() {
        const form = document.getElementById('hospitalForm');
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return;
        }

        const hospitalData = {
            _id: document.getElementById('editHospitalId').value,
            nom_etablissement: document.getElementById('editNomEtablissement').value,
            region: document.getElementById('editRegion').value,
            delegation: document.getElementById('editDelegation').value,
            commune: document.getElementById('editCommune').value,
            categorie: document.getElementById('editCategorie').value
        };

        const hospitalId = document.getElementById('hospitalId').value;

        try {
            if (hospitalId) {
                // Update existing hospital
                await this.makeRequest(`/api/hospitals/${hospitalId}`, {
                    method: 'PUT',
                    body: JSON.stringify(hospitalData)
                });
                this.showAlert('Hôpital modifié avec succès!', 'success');
            } else {
                // Create new hospital
                await this.makeRequest('/api/hospitals', {
                    method: 'POST',
                    body: JSON.stringify(hospitalData)
                });
                this.showAlert('Hôpital ajouté avec succès!', 'success');
            }

            this.closeModals();
            this.loadHospitals();
            this.loadStatistics();
        } catch (error) {
            console.error('Failed to save hospital:', error);
        }
    }

    deleteHospital(hospitalId) {
        document.getElementById('deleteHospitalId').value = hospitalId;
        const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
    }

    async confirmDelete() {
        const hospitalId = document.getElementById('deleteHospitalId').value;
        
        try {
            await this.makeRequest(`/api/hospitals/${hospitalId}`, {
                method: 'DELETE'
            });
            
            this.showAlert('Hôpital supprimé avec succès!', 'success');
            this.closeModals();
            this.loadHospitals();
            this.loadStatistics();
        } catch (error) {
            console.error('Failed to delete hospital:', error);
        }
    }

    // Data Management
    loadDataFile() {
        document.getElementById('jsonFileInput').click();
    }

    async handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        if (!file.name.endsWith('.json')) {
            this.showAlert('Veuillez sélectionner un fichier JSON valide.', 'danger');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/load_data', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();
            
            if (response.ok) {
                this.showAlert(result.message, 'success');
                this.loadHospitals();
                this.loadStatistics();
            } else {
                this.showAlert(result.error, 'danger');
            }
        } catch (error) {
            console.error('File upload failed:', error);
            this.showAlert('Erreur lors du chargement du fichier.', 'danger');
        }

        // Reset file input
        event.target.value = '';
    }

    async createSampleData() {
        try {
            const result = await this.makeRequest('/create_sample', {
                method: 'POST'
            });
            
            this.showAlert(result.message, 'success');
            this.loadHospitals();
            this.loadStatistics();
        } catch (error) {
            console.error('Failed to create sample data:', error);
        }
    }

    async exportData() {
        try {
            const hospitals = await this.makeRequest('/export_data');
            const dataStr = JSON.stringify(hospitals, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            
            const link = document.createElement('a');
            link.href = URL.createObjectURL(dataBlob);
            link.download = `moroccan_hospitals_${new Date().toISOString().split('T')[0]}.json`;
            link.click();
            
            this.showAlert('Données exportées avec succès!', 'success');
        } catch (error) {
            console.error('Export failed:', error);
        }
    }

    // Statistics
    async loadStatistics() {
        try {
            const stats = await this.makeRequest('/api/statistics');
            this.renderStatistics(stats);
        } catch (error) {
            console.error('Failed to load statistics:', error);
        }
    }

    renderStatistics(stats) {
        // Update overview cards
        document.getElementById('totalHospitals').textContent = stats.total_hospitals || 0;
        document.getElementById('totalRegions').textContent = Object.keys(stats.regions || {}).length;
        document.getElementById('totalDelegations').textContent = Object.keys(stats.delegations || {}).length;
        document.getElementById('totalCategories').textContent = Object.keys(stats.categories || {}).length;

        // Render charts if available
        this.renderRegionChart(stats.regions || {});
        this.renderCategoryChart(stats.categories || {});
    }

    renderRegionChart(regionData) {
        const ctx = document.getElementById('regionChart');
        if (!ctx) return;

        const labels = Object.keys(regionData);
        const data = Object.values(regionData);

        if (window.regionChart) {
            window.regionChart.destroy();
        }

        window.regionChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
                        '#9966FF', '#FF9F40', '#C9CBCF', '#4BC0C0'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    }
                }
            }
        });
    }

    renderCategoryChart(categoryData) {
        const ctx = document.getElementById('categoryChart');
        if (!ctx) return;

        const labels = Object.keys(categoryData);
        const data = Object.values(categoryData);

        if (window.categoryChart) {
            window.categoryChart.destroy();
        }

        window.categoryChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Nombre d\'hôpitaux',
                    data: data,
                    backgroundColor: '#36A2EB',
                    borderColor: '#2196F3',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }

    // Utility Methods
    populateForm(hospital) {
        document.getElementById('editHospitalId').value = hospital._id || hospital.id || '';
        document.getElementById('editNomEtablissement').value = hospital.nom_etablissement || '';
        document.getElementById('editRegion').value = hospital.region || '';
        document.getElementById('editDelegation').value = hospital.delegation || '';
        document.getElementById('editCommune').value = hospital.commune || '';
        document.getElementById('editCategorie').value = hospital.categorie || '';
    }

    resetForm() {
        const form = document.getElementById('hospitalForm');
        if (form) {
            form.reset();
            form.classList.remove('was-validated');
        }
        
        // Make form editable
        document.querySelectorAll('#hospitalForm input, #hospitalForm select').forEach(el => {
            el.removeAttribute('readonly');
            el.removeAttribute('disabled');
        });
        
        document.getElementById('saveHospitalBtn').style.display = 'block';
    }

    closeModals() {
        document.querySelectorAll('.modal').forEach(modal => {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        });
    }

    showAlert(message, type = 'info') {
        const alertContainer = document.getElementById('alertContainer');
        if (!alertContainer) {
            console.log(`${type.toUpperCase()}: ${message}`);
            return;
        }

        const alertId = 'alert-' + Date.now();
        const alertHTML = `
            <div class="alert alert-${type} alert-dismissible fade show" role="alert" id="${alertId}">
                <i class="bi bi-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-triangle' : 'info-circle'}"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;

        alertContainer.insertAdjacentHTML('beforeend', alertHTML);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            const alert = document.getElementById(alertId);
            if (alert) {
                alert.remove();
            }
        }, 5000);
    }

    showLoading(show) {
        const loader = document.getElementById('loadingSpinner');
        if (loader) {
            loader.style.display = show ? 'block' : 'none';
        }
    }
}

// Initialize the application
let hospitalManager;

document.addEventListener('DOMContentLoaded', function() {
    hospitalManager = new HospitalManager();
    
    console.log('🏥 Moroccan Hospitals Management System Initialized');
    console.log('📊 TinyDB NoSQL Database Interface Ready');
});

// Export for global access
window.hospitalManager = hospitalManager;