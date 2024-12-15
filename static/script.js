document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("product-form");
    const inventoryBody = document.getElementById("inventory-body");


    async function fetchProducts() {
        const response = await fetch("/productos");
        const productos = await response.json();
        inventoryBody.innerHTML = "";
        Object.values(productos).forEach(producto => {
            const row = document.createElement("tr");
            row.innerHTML = `
                <td>${producto.codigo}</td>
                <td>${producto.nombre}</td>
                <td>${producto.cantidad}</td>
                <td>${producto.fecha_vencimiento}</td>
                <td>
                    <button onclick="deleteProduct('${producto.codigo}')">Eliminar</button>
                </td>
            `;
            inventoryBody.appendChild(row);
        });
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(form);
        const producto = Object.fromEntries(formData);
        const response = await fetch("/productos", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(producto),
        });
        if (response.ok) {
            alert("Producto agregado exitosamente");
            form.reset();
            fetchProducts();
        } else {
            const error = await response.json();
            alert(error.error);
        }
    });


    window.deleteProduct = async (codigo) => {
        if (confirm("¿Estás seguro de eliminar este producto?")) {
            const response = await fetch(`/productos/${codigo}`, {
                method: "DELETE",
            });
            if (response.ok) {
                alert("Producto eliminado exitosamente");
                fetchProducts();
            } else {
                const error = await response.json();
                alert(error.error);
            }
        }
    };


    fetchProducts();
});
