import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { generateQuestion, resetQuestion } from "../redux/actions";
import "./Questionnaire.css";

const Questionnaire = () => {
  const [url, setUrl] = useState("");
  const dispatch = useDispatch();
  const questionData = useSelector((state) => state?.question);
  const [isUrlValid, setIsUrlValid] = useState(true);
  const [responses, setResponses] = useState({});
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  const validateUrl = (url) => {
    const regex = /^(https?:\/\/)([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/[^\s]*)?$/;
    return regex.test(url);
  };

  const handleSubmitForm = (e) => {
    e.preventDefault();
    dispatch(resetQuestion());

    if (url) {
      dispatch(generateQuestion(url));
    }
  };

  const handleURLChange = (e) => {
    const inputUrl = e.target.value;
    setUrl(inputUrl);

    if (inputUrl && !validateUrl(inputUrl)) {
      setIsUrlValid(false);
    } else {
      setIsUrlValid(true);
    }

    if (!inputUrl) {
      dispatch(resetQuestion());
    }
  };

  const handleOptionChange = (option) => {
    setResponses((prevResponses) => ({
      ...prevResponses,
      [currentQuestionIndex]: option,
    }));
  };

  const handleNextQuestion = () => {
    setCurrentQuestionIndex((prevIndex) => prevIndex + 1);
  };

  const handlePreviousQuestion = () => {
    setCurrentQuestionIndex((prevIndex) => prevIndex - 1);
  };

  const handleSubmitAnswers = (e) => {
    e.preventDefault();
    console.log("User Responses:", responses);
  };

  return (
    <div className="background">
      {/* Progress Bar */}
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{
            width: `${
              ((currentQuestionIndex + 1) / questionData.questions.length) * 100
            }%`,
          }}
        ></div>
      </div>

      {/* Form Container */}
      <div className="form-container">
        <h1 className="heading">Get to Know You Better</h1>
        <form onSubmit={handleSubmitForm} className="url-form">
          <input
            type="text"
            className={`url-input ${!isUrlValid ? "invalid" : ""}`}
            value={url}
            onChange={handleURLChange}
            placeholder="Enter website URL"
            required
          />
          <p className="url-info">
            Please enter a valid URL starting with <strong>http://</strong> or{" "}
            <strong>https://</strong>.
          </p>
          <button
            type="submit"
            className={`btn-primary ${
              !url || !isUrlValid ? "btn-disabled" : ""
            }`}
            disabled={!url || !isUrlValid}
          >
            Start Questionnaire
          </button>
        </form>

        {questionData.loading && (
          <div className="loading-text">
            We are processing your request. You will be presented with a
            questionnaire once the process has been completed.
          </div>
        )}
        {questionData.questions && questionData.questions.length > 0 && (
          <div className="question-card">
            <h2 className="question-title">
              {questionData.questions[currentQuestionIndex]?.question}
            </h2>
            <ul className="options-list">
              {questionData.questions[currentQuestionIndex].options.map(
                (option, index) => (
                  <li key={index} className="option-item">
                    <label className="option-label">
                      <input
                        type="radio"
                        name={`question-${currentQuestionIndex}`}
                        value={option}
                        checked={responses[currentQuestionIndex] === option}
                        onChange={() => handleOptionChange(option)}
                      />
                      <span className="option-text">{option}</span>
                    </label>
                  </li>
                )
              )}
            </ul>
            <div className="button-group">
              <button
                className="btn-secondary"
                onClick={handlePreviousQuestion}
                style={{
                  visibility: currentQuestionIndex === 0 ? "hidden" : "visible",
                }}
              >
                Previous
              </button>

              {currentQuestionIndex < questionData.questions.length - 1 ? (
                <button className="btn-primary" onClick={handleNextQuestion}>
                  Next Question
                </button>
              ) : (
                <button className="btn-primary" onClick={handleSubmitAnswers}>
                  Submit Answers
                </button>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Questionnaire;
