document.addEventListener("DOMContentLoaded", () => {
    // Feather icons
    feather.replace();

    // انیمیشن کارت‌ها
    animateCards();
});

// Toast نمایش
function showToast(message, type = "primary") {
    const toastEl = document.getElementById("liveToast");
    const toastMsg = document.getElementById("toastMessage");

    toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
    toastMsg.textContent = message;

    new bootstrap.Toast(toastEl).show();
}

// انیمیشن ظاهر شدن کارت‌ها
function animateCards() {
    const cards = document.querySelectorAll(".customer-card");
    cards.forEach((card, i) => {
        setTimeout(() => card.classList.add("animate"), i * 100);
    });
}

// مدیریت حذف با Modal
let deleteUrl = null;
let deleteCard = null;

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("delete-btn")) {
        deleteUrl = e.target.dataset.url;
        deleteCard = e.target.closest(".col");

        const confirmModalEl = document.getElementById('confirmDeleteModal');
        const confirmModal = new bootstrap.Modal(confirmModalEl);
        confirmModal.show();
    }
});

document.getElementById("confirmDeleteBtn").addEventListener("click", function () {
    if (!deleteUrl) return;

    fetch(deleteUrl, {
        method: "POST",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value
        }
    })
    .then(res => res.json())
    .then(data => {
        if (data.success && deleteCard) {
            deleteCard.remove();
            showToast("مشتری با موفقیت حذف شد!", "success");
        } else {
            showToast(data.error || "خطا در حذف!", "danger");
        }

        bootstrap.Modal.getInstance(document.getElementById('confirmDeleteModal')).hide();
        deleteUrl = null;
        deleteCard = null;
    })
    .catch(() => showToast("مشکل در اتصال به سرور!", "danger"));
});

// مدیریت تسویه حساب با Modal
let settleCustomerUrl = null;

document.addEventListener("click", function (e) {
    if (e.target.classList.contains("pay-btn")) {
        const btn = e.target;
        settleCustomerUrl = btn.dataset.url; // از data-url استفاده می‌کنیم
        document.getElementById("settleCustomerId").value = btn.dataset.id;

        const modal = new bootstrap.Modal(document.getElementById("settleModal"));
        modal.show();
    }
});

document.getElementById("settleForm").addEventListener("submit", function (e) {
    e.preventDefault();

    const amount = parseFloat(document.getElementById("settleAmount").value);
    const operation = document.querySelector('input[name="operation"]:checked').value;

    if (isNaN(amount) || amount <= 0 || !settleCustomerUrl) return;

    fetch(settleCustomerUrl, {
        method: "POST",
        headers: {
            "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ amount, operation })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showToast("تراکنش با موفقیت ثبت شد!", "success");

            const card = document.querySelector(`.pay-btn[data-id='${document.getElementById("settleCustomerId").value}']`).closest(".col");
            card.querySelector(".amount").textContent = data.new_amount + " تومان";
            if (data.is_paid) card.classList.add("border-success");
        } else {
            showToast(data.error || "خطا در ثبت تراکنش!", "danger");
        }

        bootstrap.Modal.getInstance(document.getElementById("settleModal")).hide();
        settleCustomerUrl = null;
        document.getElementById("settleForm").reset();
    })
    .catch(() => showToast("خطای سرور!", "danger"));
});
