import axios from "axios";

export const generateQuestion = (url) => async (dispatch) => {
  try {
    dispatch({ type: "GENERATE_QUESTION_REQUEST" });

    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };
    const response = await axios.post(
      "http://localhost:5001/generate-question",
      { url, save_to_db: true },
      config
    );
    dispatch({ type: "GENERATE_QUESTION_SUCCESS", payload: response.data });
  } catch (error) {
    dispatch({ type: "GENERATE_QUESTION_FAIL", payload: error.message });
  }
};

export const resetQuestion = () => {
  return { type: "RESET_QUESTION" };
};
