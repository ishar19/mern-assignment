import React, { useContext } from "react";
import HomeBanner from "../components/Home/HomeBanner";
import HomeUser from "../components/Home/HomeUser";
import Location from "../components/Home/Location";
import Navbar from "../components/global/Navbar";
import RecentScans from "../components/Home/RecentScans";
import Articles from "../components/Home/Articles";

import { UserContext } from "../Context/UserProvider";
import SEO from "../components/global/SEO";

const Home = () => {
  const user = useContext(UserContext);
  // const title = "RecyclOps";
  // useEffect(() => {
  //   document.title = title;
  // }, []);

  return (
    <>
      <SEO
        title="RecyclOps"
        description="AI powered tool for waste management"
        authors="Ishar Jain Prabkirat Singh Bhavya Giri Diksha Raj"
        name="RecyclOps"
        keywords="Trash Disposal AI React Sustainable Development Game"
      />
      <div className="bg-gradient-to-l from-[#34A85366]/40 to-[#34A85366]/10 px-[5vw] pt-5 pb-16 overflow-x-hidden">
        <div className="flex items-center justify-between">
          <HomeUser />
          <Location />
        </div>
        <HomeBanner />
        <RecentScans user={user} />
        <Articles user={user} />
      </div>
      <Navbar />
    </>
  );
};
export default Home;
