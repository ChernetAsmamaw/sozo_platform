import React from "react";
import logo from "../../assets/logo-long.png";

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-light text-white py-4 border-top">
      <div className="container">
        <div className="row align-items-center text-center text-md-start">
          <div className="col-md-5 mb-3 mb-md-0">
            <div className="text-muted">
              <div
                className="text-primary-hover"
                style={{ textDecoration: "none" }}
              >
                &copy; {currentYear} The Sozo Foundation
              </div>
              <a
                href="https://www.github.com/chernetAsmamaw"
                target="_blank"
                rel="noopener noreferrer"
                className="d-flex align-items-center mt-2"
                style={{
                  color: "gray",
                  textDecoration: "none",
                  fontFamily: "cursive",
                }}
              >
                <i className="fab fa-github me-2" />
                Developed by Chernet
              </a>
            </div>
          </div>
          <div className="col-md-3 mb-3 mb-md-0 text-center">
            <img src={logo} style={{ width: "120px" }} alt="footer logo" />
          </div>
          <div className="col-md-4">
            <ul className="nav justify-content-center justify-content-md-end">
              <li className="nav-item">
                <a
                  className="nav-link px-2 fs-4"
                  href="https://facebook.com/thesozofoundation"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "none", color: "#3b5998" }}
                >
                  <i className="fab fa-facebook-square" />
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link px-2 fs-4"
                  href="https://twitter.com/thesozofoundation"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "none", color: "#1DA1F2" }}
                >
                  <i className="fab fa-twitter-square" />
                </a>
              </li>
              <li className="nav-item">
                <a
                  className="nav-link px-2 fs-4"
                  href="https://youtube.com/@thesozofoundation"
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ textDecoration: "none", color: "#FF0000" }}
                >
                  <i className="fab fa-youtube-square" />
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer;
