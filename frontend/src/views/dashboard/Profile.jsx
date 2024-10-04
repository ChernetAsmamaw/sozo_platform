import React, { useState, useEffect } from "react";
import Header from "../partials/Header";
import Footer from "../partials/Footer";
import { Link } from "react-router-dom";

import apiInstance from "../../utils/axios";
import useUserData from "../../plugin/useUserData";
import Toast from "../../plugin/Toast";
import moment from "moment";

function Profile() {
  const [profileData, setProfileData] = useState({
    image: null,
    full_name: "",
    about: "",
    bio: "",
    facebook: "",
    whatsapp: "",
    instagram: "",
    linkedin: "",
    country: "",
    city: "",
    date: "",
  });
  const userId = useUserData()?.user_id;

  // To display the image preview right after the user selects an image
  const [imagePreview, setImagePreview] = useState("");
  const [loading, setLoading] = useState(false);

  const fetchProfile = () => {
    apiInstance.get(`user/profile/${userId}/`).then((res) => {
      setProfileData(res.data);
    });
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  // This is when user changes the profile data
  const handleProfileChange = (event) => {
    setProfileData({
      ...profileData,
      [event.target.name]: event.target.value,
    });
  };

  // This is when user puts an image for profile
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    setProfileData({
      ...profileData,
      [event.target.name]: selectedFile,
    });

    const reader = new FileReader();
    reader.onloadend = () => {
      setImagePreview(reader.result);
    };
    if (selectedFile) {
      reader.readAsDataURL(selectedFile);
    }
  };

  // This is when user submits the form
  const handleFormSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const res = await apiInstance.get(`user/profile/${userId}/`);

    const formData = new FormData();

    // If the profile image is not the same as the one in the database, then add the new image to the form data
    if (profileData.image && profileData.image !== res.data.image) {
      formData.append("image", profileData.image);
    }
    formData.append("full_name", profileData.full_name);
    formData.append("about", profileData.about);
    formData.append("bio", profileData.bio);
    formData.append("facebook", profileData.facebook);
    formData.append("whatsapp", profileData.whatsapp);
    formData.append("instagram", profileData.instagram);
    formData.append("linkedin", profileData.linkedin);
    formData.append("country", profileData.country);
    formData.append("city", profileData.city);

    try {
      const res = await apiInstance.patch(`user/profile/${userId}/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      Toast("success", "Profile updated successfully", "");
      setLoading(false);
    } catch (error) {
      console.error("Error updating profile:", error);
      Toast("error", "An Error Occured", "");
    }
  };

  console.log(profileData);
  return (
    <>
      <Header />
      <section className="pt-5 pb-5">
        <div className="container">
          <div className="row mt-0 mt-md-4">
            <div className="col-lg-12 col-md-8 col-12">
              {/* Card */}
              <div className="card">
                {/* Card header */}
                <div className="card-header">
                  <h3 className="mb-0">Profile Details</h3>
                  <p className="mb-0">
                    You have full control to manage your own account setting.
                  </p>
                </div>
                {/* Card body */}
                <form className="card-body" onSubmit={handleFormSubmit}>
                  <div className="d-lg-flex align-items-center justify-content-between">
                    <div className="d-flex align-items-center mb-4 mb-lg-0">
                      <img
                        src={imagePreview || profileData?.image}
                        id="img-uploaded"
                        className="avatar-xl rounded-circle"
                        alt="avatar"
                        style={{
                          width: "100px",
                          height: "100px",
                          borderRadius: "50%",
                          objectFit: "cover",
                        }}
                      />

                      <div className="ms-3">
                        <h4 className="mb-0">Your Profile Picture</h4>
                        <p className="mb-0">
                          PNG or JPG no bigger than 800px wide and tall.
                        </p>
                        <input
                          type="file"
                          name="image"
                          className="form-control mt-3"
                          onChange={handleFileChange}
                        />
                      </div>
                    </div>
                  </div>
                  <hr className="my-5" />
                  <div>
                    <h4 className="mb-0">Personal Details</h4>
                    <p className="mb-4">
                      Edit your personal information and address.
                    </p>
                    {/* Form */}
                    <div className="row gx-3">
                      {/* First name */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="fname">
                          Full Name
                        </label>
                        <input
                          type="text"
                          id="fname"
                          className="form-control"
                          placeholder="First Name"
                          required=""
                          onChange={handleProfileChange}
                          name="full_name"
                          value={profileData?.full_name}
                        />
                        <div className="invalid-feedback">
                          Please enter first name.
                        </div>
                      </div>
                      {/* Last name */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="lname">
                          About Me
                        </label>
                        <textarea
                          onChange={handleProfileChange}
                          name="about"
                          id=""
                          cols="30"
                          value={profileData?.about}
                          rows="5"
                          className="form-control"
                        ></textarea>
                      </div>
                      {/* Bio */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Bio
                        </label>
                        <input
                          type="text"
                          id="bio"
                          className="form-control"
                          placeholder="Bio"
                          required=""
                          value={profileData?.bio}
                          onChange={handleProfileChange}
                          name="bio"
                        />
                        <div className="invalid-feedback">
                          Please choose country.
                        </div>
                      </div>
                      {/* Country */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Country
                        </label>
                        <input
                          type="text"
                          id="country"
                          className="form-control"
                          placeholder="Country"
                          required=""
                          value={profileData?.country}
                          onChange={handleProfileChange}
                          name="country"
                        />
                        <div className="invalid-feedback">
                          Please choose country.
                        </div>
                      </div>
                      {/* City */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          City
                        </label>
                        <input
                          type="text"
                          id="city"
                          className="form-control"
                          placeholder="City"
                          required=""
                          value={profileData?.city}
                          onChange={handleProfileChange}
                          name="city"
                        />
                        <div className="invalid-feedback">
                          Please choose city.
                        </div>
                      </div>
                      {/* Facebook */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Facebook
                        </label>
                        <input
                          type="text"
                          id="facebook"
                          className="form-control"
                          placeholder="Facebook"
                          required=""
                          value={profileData?.facebook}
                          onChange={handleProfileChange}
                          name="facebook"
                        />
                      </div>
                      {/* Instagram */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Instagram
                        </label>
                        <input
                          type="text"
                          id="instagram"
                          className="form-control"
                          placeholder="Instagram"
                          required=""
                          value={profileData?.instagram}
                          onChange={handleProfileChange}
                          name="instagram"
                        />
                      </div>
                      {/* Linkedin */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Linkedin
                        </label>
                        <input
                          type="text"
                          id="linkedin"
                          className="form-control"
                          placeholder="Linkedin"
                          required=""
                          value={profileData?.linkedin}
                          onChange={handleProfileChange}
                          name="linkedin"
                        />
                      </div>
                      {/* Whatsapp */}
                      <div className="mb-3 col-12 col-md-12">
                        <label className="form-label" htmlFor="editCountry">
                          Whatsapp
                        </label>
                        <input
                          type="text"
                          id="whatsapp"
                          className="form-control"
                          placeholder="Whatsapp"
                          required=""
                          value={profileData?.whatsapp}
                          onChange={handleProfileChange}
                          name="whatsapp"
                        />
                      </div>
                      {/* Date */}
                      <hr />
                      <div className="mb-3 col-12 col-md-12 text-center">
                        <p>
                          You've been with us since{" "}
                          {moment(profileData?.date).format("MMMM Do, YYYY")}
                        </p>
                      </div>
                      <hr />
                      <div className="col-12">
                        {/* Button */}
                        <button className="btn btn-primary" type="submit">
                          Update Profile <i className="fas fa-check-circle"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>
      <Footer />
    </>
  );
}

export default Profile;
