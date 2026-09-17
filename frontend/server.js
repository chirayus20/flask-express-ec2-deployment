const express = require("express");
const axios = require("axios");
const fs = require("fs");

const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static("public"));

app.get("/health", (req, res) => {
    res.status(200).json({ status: "ok" });
});

// when user submits the form
app.post("/submit", async (req, res) => {
    const backendUrl = process.env.BACKEND_URL || "http://localhost:9000";

    try {
        const response = await axios.post(
            backendUrl + "/process",
            req.body
        );

        if (response.data.success) {
            return res.redirect("/success.html");
        }

    } catch (err) {
        let message = "Something went wrong";

        if (err.response) {
            message = err.response.data.message;
        }

        let page = fs.readFileSync("public/index.html", "utf8");

        page = page.replace(
            "<!-- ERROR_MESSAGE -->",
            `<div class="error-alert">${message}</div>
            <script>
                history.replaceState(null, "", "/");
            </script>`
        );

        return res.send(page);
    }
});

app.listen(8000, () => {
    console.log("Frontend running on port 8000");
});