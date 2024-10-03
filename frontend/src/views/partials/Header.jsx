import React from "react";
import { Link } from "react-router-dom";
import { useAuthStore } from "../../store/auth";
import logo from "../../assets/logo.png";

function Header() {
  const [isLoggedIn, user] = useAuthStore((state) => [
    state.isLoggedIn,
    state.user,
  ]);
  return (
    <header className="navbar-dark bg-light navbar-sticky header-static border-bottom">
      <nav className="navbar navbar-expand-lg">
        <div className="container">
          <Link className="navbar-brand" to="/">
            <img
              className="navbar-brand-item dark-mode-item"
              src={logo}
              style={{ width: "100px" }}
              alt="logo"
            />
          </Link>
          <button
            className="navbar-toggler ms-auto"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarCollapse"
            aria-controls="navbarCollapse"
            aria-expanded="false"
            aria-label="Toggle navigation"
            style={{ borderColor: "black" }}
          >
            <span className="h6 d-none d-sm-inline-block text-dark">Menu</span>
            <i className="bi bi-list fs-5 text-dark px-2 t-4"> </i>
          </button>
          <div className="collapse navbar-collapse" id="navbarCollapse">
            <div className="nav mt-3 mt-lg-0 px-4 flex-nowrap align-items-center">
              <div className="nav-item w-100">
                <form className="rounded position-relative">
                  <input
                    className="form-control pe-5 bg-light text-dark"
                    type="search"
                    placeholder="Search Articles"
                    aria-label="Search"
                  />
                  <Link
                    to={"/search/"}
                    className="btn bg-transparent border-0 px-2 py-0 position-absolute top-50 end-0 translate-middle-y text-dark"
                    type="submit"
                  >
                    <i className="bi bi-search fs-5"> </i>
                  </Link>
                </form>
              </div>
            </div>
            <ul className="navbar-nav navbar-nav-scroll ms-auto text-dark">
              <li className="nav-item dropdown">
                <Link className="nav-link active text-dark" to="/">
                  Home
                </Link>
              </li>
              <li className="nav-item dropdown">
                <Link className="nav-link active text-dark" to="/category/">
                  Category
                </Link>
              </li>
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle active text-dark"
                  href="#"
                  id="pagesMenu"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  Pages
                </a>
                <ul className="dropdown-menu" aria-labelledby="pagesMenu">
                  <li>
                    <Link className="dropdown-item text-dark" to="/about/">
                      <i className="bi bi-person-lines-fill"></i> About
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item text-dark" to="/contact/">
                      <i className="bi bi-telephone-fill"></i> Contact
                    </Link>
                  </li>
                </ul>
              </li>
              <li className="nav-item dropdown">
                <a
                  className="nav-link dropdown-toggle active text-dark"
                  href="#"
                  id="pagesMenu"
                  data-bs-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >
                  Dashboard
                </a>
                <ul className="dropdown-menu" aria-labelledby="pagesMenu">
                  <li>
                    <Link className="dropdown-item text-dark" to="/dashboard/">
                      <i className="fas fa-user"></i> Dashboard
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item text-dark" to="/posts/">
                      <i className="bi bi-grid-fill"></i> Posts
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item text-dark" to="/add-post/">
                      <i className="fas fa-plus-circle"></i> Add Post
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item text-dark" to="/comments/">
                      <i className="bi bi-chat-left-quote-fill"></i> Comments
                    </Link>
                  </li>
                  <li>
                    <Link
                      className="dropdown-item text-dark"
                      to="/notifications/"
                    >
                      <i className="fas fa-bell"></i> Notifications
                    </Link>
                  </li>
                  <li>
                    <Link className="dropdown-item text-dark" to="/profile/">
                      <i className="fas fa-user-gear"></i> Profile
                    </Link>
                  </li>
                </ul>
              </li>
              <li className="nav-item">
                {isLoggedIn() ? (
                  <>
                    <Link
                      to={"/dashboard/"}
                      className="btn btn-secondary text-light"
                      href="dashboard.html"
                    >
                      Dashboard <i className="bi bi-grid-fill"></i>
                    </Link>
                    <Link
                      to={"/logout/"}
                      className="btn btn-danger ms-2 text-light"
                      href="dashboard.html"
                    >
                      Logout <i className="fas fa-sign-out-alt"></i>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link
                      to={"/register/"}
                      className="btn btn-success text-light"
                      href="dashboard.html"
                    >
                      Register <i className="fas fa-user-plus"></i>
                    </Link>
                    <Link
                      to={"/login/"}
                      className="btn btn-success ms-2 text-light"
                      href="dashboard.html"
                    >
                      Login <i className="fas fa-sign-in-alt"></i>
                    </Link>
                  </>
                )}
              </li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  );
}

export default Header;
