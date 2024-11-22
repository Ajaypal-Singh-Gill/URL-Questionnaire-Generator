import axios from "axios";

const BASE_URL = process.env.REACT_APP_BE_BASE_URL || "http://localhost:5001";

export const generateQuestion = (url) => async (dispatch) => {
  try {
    dispatch({ type: "GENERATE_QUESTION_REQUEST" });

    const config = {
      headers: {
        "Content-Type": "application/json",
      },
    };

    // // Step 1: Trigger the question generation
    // const response = await axios.post(
    //   `${BASE_URL}/generate-question`,
    //   { url, save_to_db: true },
    //   config
    // );

    // Step 2: Poll the backend until questions are populated
    const pollForQuestions = async () => {
      try {
        const resultResponse = await axios.post(
          `${BASE_URL}/generate-question`,
          { url, save_to_db: false }, // Same endpoint but don't re-trigger task
          config
        );

        if (resultResponse.data.questions.length > 0) {
          // Questions are ready, dispatch success
          dispatch({
            type: "GENERATE_QUESTION_SUCCESS",
            payload: resultResponse.data,
          });
        } else {
          // Questions not ready, poll again after a delay
          setTimeout(pollForQuestions, 3000); // Poll every 3 seconds
        }
      } catch (error) {
        console.error("Polling error:", error.message);
        dispatch({ type: "GENERATE_QUESTION_FAIL", payload: error.message });
      }
    };

    // Start polling
    pollForQuestions();
  } catch (error) {
    // Handle initial request failure
    dispatch({ type: "GENERATE_QUESTION_FAIL", payload: error.message });
  }
};

export const resetQuestion = () => {
  return { type: "RESET_QUESTION" };
};
