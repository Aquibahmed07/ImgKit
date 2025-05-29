body {
  font-family: 'Roboto', sans-serif;
  background: #f0f8f0;
  margin: 0;
  padding: 0;
  color: #222;
}
header {
  background: #0b3e47;
  color: #fff;
  padding: 1rem 0;
  text-align: center;
  position: sticky;
  top: 0;
  z-index: 10;
}

.logo {
  font-family: 'Playfair Display', serif;
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

header nav ul {
  list-style: none;
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 0;
  margin: 0;
}

header nav ul li a {
  color: #fff;
  text-decoration: none;
  font-weight: bold;
  font-size: 1rem;
  transition: color 0.2s;
}

header nav ul li a:hover {
  color: #4caf50;
}

.hero {
  padding: 2rem 1rem 1rem 1rem;
  text-align: center;
  background: #e8f5e9;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.hero p {
  font-size: 1.2rem;
  color: #333;
}

.tools-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 2rem;
  margin: 2rem;
}

.tool-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  padding: 2rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  min-width: 320px;
  max-width: 340px;
  flex: 1 1 320px;
  min-height: 340px;
  position: relative;
  transition: box-shadow 0.2s;
}

.tool-card:hover {
  box-shadow: 0 8px 24px rgba(0,0,0,0.13);
  transform: translateY(-4px) scale(1.01);
}

.tool-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin-bottom: 1rem;
  color: #222;
}

.coming-soon {
  margin-top: 1.5rem;
  background: #e0e0e0;
  color: #888;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
}

.tool-card h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.2rem;
  margin: 0.5rem 0 0.5rem 0;
}

.tool-card p {
  font-size: 1rem;
  color: #444;
  margin-bottom: 1rem;
}

.tool-card form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  width: 100%;
}

.tool-card input[type="file"],
.tool-card input[type="number"] {
  padding: 10px;
  border: 1px solid #dcdcdc;
  border-radius: 6px;
  background: #f9f9f9;
}

.tool-card button {
  padding: 12px 0;
  background: #4caf50;
  color: #fff;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: background 0.3s;
}

.tool-card button:hover {
  background: #388e3c;
}

.download-link {
  margin-top: 1rem;
}

.download-link a {
  display: inline-block;
  padding: 10px 20px;
  background: #0b3e47;
  color: #fff;
  border-radius: 5px;
  text-decoration: none;
  font-weight: bold;
  transition: background 0.3s;
}

.download-link a:hover {
  background: #4caf50;
}

footer {
  background: #0b3e47;
  color: #fff;
  text-align: center;
  padding: 2rem 1rem 1rem 1rem;
  margin-top: 2rem;
}

.footer-content {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: flex-start;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

.footer-logo h2 {
  font-family: 'Playfair Display', serif;
  font-size: 1.8rem;
  margin-bottom: 1rem;
}

.footer-contact h3 {
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}

.footer-contact p {
  font-size: 0.95rem;
  margin: 0.3rem 0;
}

.footer-social {
  display: flex;
  gap: 0.5rem;
}

.footer-social a {
  color: #fff;
  font-size: 1.5rem;
  text-decoration: none;
  transition: color 0.3s;
  margin: 0 0.3rem;
}

.footer-social a:hover {
  color: #4caf50;
}

.footer-bottom {
  margin-top: 2rem;
  font-size: 0.8rem;
  border-top: 1px solid rgba(255,255,255,0.2);
  padding-top: 1rem;
}

@media (max-width: 900px) {
  .tools-grid {
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }
  .footer-content {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}

@media (max-width: 1100px) {
  .tools-grid {
    flex-direction: column;
    align-items: center;
    gap: 2rem;
  }
  .tool-card {
    max-width: 95vw;
    min-width: 280px;
  }
}

@media (max-width: 600px) {
  .tool-card {
    padding: 1.2rem 0.5rem;
    min-width: 90vw;
    max-width: 98vw;
  }
  .tools-grid {
    margin: 1rem 0.2rem;
    gap: 1rem;
  }
}
