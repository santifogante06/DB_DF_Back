const fetchLastProducts = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/dashboard/stock-movement?sort_by=action_date_time&order=desc&limit=3');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        data.forEach(element => {
            action = element.action_function;
            if (action === 'add') {
                document.getElementById('stock-listbox').innerHTML += `<li>+ ${element.product_name} | Stock moved: ${element.stock_moved}</li>`;
            }
            else if (action === 'remove') {
                document.getElementById('stock-listbox').innerHTML += `<li>- ${element.product_name} | Stock moved: ${element.stock_moved}</li>`;
            }
        });
        return data;
    } catch (error) {
        console.error('Error fetching last products:', error);
        return [];
    }
};

fetchLastProducts();

const btnAdd = document.getElementById('btn-add');
const formBarcode = document.getElementById('form-barcode');
const btnRemove = document.getElementById('btn-remove');
const formBarcodeRemove = document.getElementById('form-barcode-remove');
const closeIcons = document.getElementsByClassName('close-icon');
const cancelButton = document.getElementById('cancel-button');
const updateButton = document.getElementById('update-button');
const cancelButtonRemove = document.getElementById('cancel-button-remove');
const updateButtonRemove = document.getElementById('update-button-remove');

btnAdd.addEventListener('click', async () => {
    formBarcode.showModal();
    Array.from(closeIcons).forEach(icon => {
        icon.addEventListener('click', () => {
            formBarcode.close();
        });
    });
});

btnRemove.addEventListener('click', async () => {
    formBarcodeRemove.showModal();
    Array.from(closeIcons).forEach(icon => {
        icon.addEventListener('click', () => {
            formBarcodeRemove.close();
        });
    });
});

formBarcode.addEventListener('submit', async (event) => {
    event.preventDefault();
    const barcode = document.getElementById('barcode').value.trim();
    if (barcode) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/dashboard/fetch-barcode/${barcode}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            formBarcode.close();
            if (Array.isArray(data) && data.length === 0) {
                document.getElementById('form-stock-barcode').value = barcode;
                document.getElementById('dialog-full').showModal();
                Array.from(closeIcons).forEach(icon => {
                    icon.addEventListener('click', () => {
                        document.getElementById('dialog-full').close();
                    });
                });
            } else if (data && data.length === 1) {
                document.getElementById('form-stock-barcode').value = barcode;
                document.getElementById('dialog-update').showModal();
                cancelButton.addEventListener('click', () => {
                    document.getElementById('dialog-update').close();
                });
            }
        } catch (error) {
            console.error('Error fetching product data:', error);
        }
    }

});

formBarcodeRemove.addEventListener('submit', async (event) => {
    event.preventDefault();
    const barcode = document.getElementById('barcode-remove').value.trim();
    if (barcode) {
        try {
            const response = await fetch(`http://127.0.0.1:8000/dashboard/fetch-barcode/${barcode}`);
            if (!response.ok) throw new Error('Network response was not ok');
            const data = await response.json();
            formBarcodeRemove.close();
            if (data && data.length === 1) {
                document.getElementById('form-stock-barcode').value = barcode;
                document.getElementById('dialog-update-remove').showModal();
                cancelButtonRemove.addEventListener('click', () => {
                    document.getElementById('dialog-update-remove').close();
                });
            } else {
                document.getElementById('dialog-not-found').showModal();
                Array.from(closeIcons).forEach(icon => {
                    icon.addEventListener('click', () => {
                        document.getElementById('dialog-not-found').close();
                    });
                });
            }
        } catch (error) {
            console.error('Error fetching product data:', error);
        }
    }
});

