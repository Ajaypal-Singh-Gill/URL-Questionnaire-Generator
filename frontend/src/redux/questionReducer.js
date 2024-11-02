const initialState = {
  loading: false,
  questions: [],
  error: null,
};

const questionReducer = (state = initialState, action) => {
  switch (action.type) {
    case "GENERATE_QUESTION_REQUEST":
      return {
        ...state,
        loading: true,
        error: null,
      };
    case "GENERATE_QUESTION_SUCCESS":
      return {
        ...state,
        loading: false,
        questions: action.payload.questions,
      };
    case "GENERATE_QUESTION_FAIL":
      return {
        ...state,
        loading: false,
        error: action.payload,
      };
    case "RESET_QUESTION":
      return {
        ...state,
        loading: false,
        questions: [], // Clear questions
        error: null,
      };
    default:
      return state;
  }
};

export default questionReducer;
