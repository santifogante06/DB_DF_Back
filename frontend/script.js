const fetchLastProducts = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/dashboard/stock-movement?sort_by=action_date_time&order=desc&limit=3');
        if (!response.ok) throw new Error('Network response was not ok');
        const data = await response.json();
        data.forEach(element => {
            action = element.action_function;
            if (action === 'add') {
                document.getElementById('stock-listbox').innerHTML += `<li>${element.product_name} | Stock moved: ${element.stock_moved}</li>`;
            }
            else if (action === 'remove') {
                document.getElementById('stock-listbox').innerHTML += `<li>${element.product_name} | Stock moved: ${element.stock_moved}</li>`;
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
const dialogFull = document.getElementById('dialog-full');
const dialogUpdate = document.getElementById('dialog-update');
const dialogUpdateRemove = document.getElementById('dialog-update-remove');

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
                dialogFull.showModal();
                Array.from(closeIcons).forEach(icon => {
                    icon.addEventListener('click', () => {
                        dialogFull.close();
                    });
                });
            } else if (data && data.length === 1) {
                document.getElementById('form-stock-barcode').value = barcode;
                dialogUpdate.showModal();
                cancelButton.addEventListener('click', () => {
                    dialogUpdate.close();
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

document.getElementById('form-full').onsubmit = async (event) => {
    event.preventDefault();
    const body = {
        product: {
            product_name: document.getElementById("product_name").value,
            product_barcode: Number(document.getElementById("form-stock-barcode").value)
        },
        location: {
            ubicaciones_row: document.getElementById("ubicaciones_row").value,
            ubicaciones_column: Number(document.getElementById("ubicaciones_column").value)
        },
        stock: {
            stock_quantity: Number(document.getElementById("stock_quantity").value)
        }
    };
    console.log(body);
    try {
        const response = await fetch('http://127.0.0.1:8000/dashboard/insert-product', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json();
            alert('❌ Error adding product:', error);
        } else {
            const result = await response.json();
            alert('✅ Product added:', result);
            dialogFull.close();
        }
        document.getElementById('stock-listbox').innerHTML = "";
        await fetchLastProducts();
    } catch (error) {
        console.error('Error adding product:', error);
    }
};

document.getElementById("form-update-add").onsubmit = async (event) => {
    event.preventDefault();
    const body = {
            product_barcode: Number(document.getElementById("form-stock-barcode").value),
            stock_moved: Number(document.getElementById("stock_moved_add").value)
    };
    console.log(body);
    try {
        const response = await fetch('http://127.0.0.1:8000/dashboard/update-product', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json();
            alert('❌ Error updating stock:', error);
        } else {
            const result = await response.json();
            alert('✅ Stock updated:', result);
            dialogUpdate.close();
        }
        document.getElementById('stock-listbox').innerHTML = "";
        await fetchLastProducts();
    } catch (error) {
        console.error('Error adding product:', error);
    }
};

document.getElementById("form-update-remove").onsubmit = async (event) => {
    event.preventDefault();
    const stockInput = Number(document.getElementById("stock_moved_remove").value);
    const stockMoved = -Math.abs(stockInput);

    const body = {
        product_barcode: Number(document.getElementById("form-stock-barcode").value),
        stock_moved: stockMoved
    };
    console.log(body);
    try {
        const response = await fetch('http://127.0.0.1:8000/dashboard/update-product', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(body),
        });
        if (!response.ok) {
            const error = await response.json();
            alert('❌ Error updating stock:', error);
        } else {
            const result = await response.json();
            alert('✅ Stock updated:', result);
            dialogUpdateRemove.close();
        }
        document.getElementById('stock-listbox').innerHTML = "";
        await fetchLastProducts();
    } catch (error) {
        console.error('Error adding product:', error);
    }
};
