document.addEventListener('DOMContentLoaded', function () {
    var dropdownInputs = document.querySelectorAll('.dropdown-input');

    dropdownInputs.forEach(function (input) {
        var dropdownMenu = input.nextElementSibling;
        var tableRows = dropdownMenu.querySelectorAll('tbody tr');

        tableRows.forEach(function (row) {
            row.addEventListener('click', function () {
                var name = this.getAttribute('data-name');
                var value = this.getAttribute('data-value');

                input.value = name + ' - ' + value;

                // Highlight selected row
                tableRows.forEach(r => r.classList.remove('selected'));
                this.classList.add('selected');

                // Hide dropdown after selection
                dropdownMenu.style.display = 'none';
            });
        });

        input.addEventListener('click', function () {
            // Toggle dropdown visibility
            if (dropdownMenu.style.display === 'none' || dropdownMenu.style.display === '') {
                dropdownMenu.style.display = 'block';
            } else {
                dropdownMenu.style.display = 'none';
            }
        });

        // Highlight the selected value if greater than zero
        var value = input.value.split(' - ')[1];
        if (value && parseFloat(value) > 0) {
            tableRows.forEach(function (row) {
                if (row.getAttribute('data-value') === value) {
                    row.classList.add('selected');
                }
            });
        }
    });

    // Hide dropdowns when clicking outside
    document.addEventListener('click', function (event) {
        dropdownInputs.forEach(function (input) {
            var dropdownMenu = input.nextElementSibling;
            if (!event.target.closest('.dropdown') && !event.target.closest('.dropdown-input')) {
                dropdownMenu.style.display = 'none';
            }
        });
    });
});