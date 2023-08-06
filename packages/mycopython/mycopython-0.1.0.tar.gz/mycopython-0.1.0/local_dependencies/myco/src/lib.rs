extern crate pest;
#[macro_use]
extern crate pest_derive;

use pest::Parser;
mod blocks;
use crate::blocks::Paragraph;

#[derive(Parser)]
#[grammar = "block.pest"]
pub struct BlockParser;

pub fn gen_html(str: &str) -> String {
    // let str = fs::read_to_string("sample.myco").unwrap();
    // println!("{}", str);
    let blocks = BlockParser::parse(Rule::input, &str)
        .unwrap()
        .next()
        .unwrap()
        .into_inner();
    // println!("{}", str);
    let mut output = vec!["".to_string()];
    for block in blocks {
        match block.as_rule() {
            Rule::block => {
                output.push("<div>".to_string());
                let _block = block.clone();
                let inner_block = _block.into_inner();
                let rule = inner_block.peek().unwrap().as_rule();
                // println!("Found block [{:?}]: {:?}", rule, block.as_span());

                match rule {
                    Rule::paragraph => {
                        let mut paragraph: Vec<Box<dyn blocks::Paragraph>> = vec![];
                        let flattened = inner_block.flatten();
                        for pair in flattened {
                            // println!("parsing internals of paragraph");
                            // println!("INNER BLOCK {:#?}", flattened);
                            // println!("{:#?}", flattened);
                            // println!("Rule: {:#?}", pair.as_rule());
                            match pair.as_rule() {
                                Rule::text => {
                                    // println!("Text: {:?}", pair.as_str());
                                    let text = blocks::PlainText {
                                        content: pair.as_str().to_string(),
                                    };
                                    // println!("Text block: {:#?}", text);
                                    paragraph.push(Box::new(text));
                                }
                                Rule::wikilink => {
                                    // println!("Wikilink: {:#?}", pair.as_str());
                                    let inner = pair.into_inner().flatten();
                                    let mut wikilink_title = "";
                                    let mut wikilink_target = "";
                                    for pair in inner {
                                        match pair.as_rule() {
                                            Rule::wikilink_target => {
                                                wikilink_target = pair.as_str().trim();
                                            }
                                            Rule::wikilink_title => {
                                                wikilink_title = pair.as_str();
                                            }
                                            _ => (),
                                        }
                                    }
                                    let target =
                                        blocks::Link::WikilinkTarget(wikilink_target.to_string());
                                    let title = wikilink_title.to_string();
                                    let wikilink = blocks::Wikilink { target, title };
                                    // print!("Wikilink Block: {:#?}", wikilink);
                                    paragraph.push(Box::new(wikilink));
                                }
                                Rule::style => {
                                    // println!("Style: {:#?}", pair.as_str());
                                    // println!("Style inner: {:#?}", pair);
                                    let pairs = pair.into_inner();
                                    for mut pair in pairs {
                                        match pair.as_rule() {
                                            Rule::italic => {
                                                pair = pair.into_inner().peek().unwrap();
                                                // println!("{}", pair.as_str());
                                                let formatted = blocks::FormattedText {
                                                    style: blocks::Style::Italic,
                                                    content: pair.as_str().to_string(),
                                                };
                                                // println!("{:#?}", formatted);
                                                paragraph.push(Box::new(formatted));
                                            }
                                            _ => (),
                                        }
                                    }
                                }
                                Rule::url => {
                                    // println!("Url: {:#?}", pair.as_str());
                                    let link = blocks::Inlinelink {
                                        target: blocks::Link::Url(pair.as_str().to_string()),
                                        title: pair.as_str().to_string(),
                                    };
                                    paragraph.push(Box::new(link));
                                }
                                _ => (),
                            }
                        }
                        // println!("{:#?}", paragraph);
                        // println!("RENDERED HTML");
                        for block in paragraph {
                            // print!("{}", block.to_html());
                            output.push(block.to_html());
                        }
                        // println!("");
                    }
                    Rule::rocket => {
                        let flattened = inner_block.flatten();
                        let mut title: String = "".to_string();
                        let mut target = blocks::Link::Url("".to_string());
                        for pair in flattened {
                            match pair.as_rule() {
                                Rule::wikilink_target => {
                                    // println!("found wikilink target: {:#?}", pair.as_str());
                                    target =
                                        blocks::Link::WikilinkTarget(pair.as_str().to_string());
                                }
                                Rule::wikilink_title => {
                                    // println!("found wikilink title: {:#?}", pair.as_str());
                                    title = pair.as_str().to_string();
                                }

                                Rule::url => println!("found url: {:#?}", pair.as_str()),
                                _ => (),
                            }
                        }
                        let link = blocks::Inlinelink { title, target };
                        // println!("{}", link.to_html());
                        output.push(link.to_html())
                    }
                    Rule::codeblock => {
                        let pairs = block.into_inner().flatten();
                        for pair in pairs {
                            match pair.as_rule() {
                                Rule::code => {
                                    // println!("{:#?}", pair.as_str());
                                    let code = blocks::Code {
                                        content: pair.as_str().to_string(),
                                    };
                                    output.push(code.to_html());
                                    // println!("{:#?}", code.to_html());
                                }
                                _ => (),
                            }
                        }
                        // println!("{:#?}", inner);
                    }
                    _ => (),
                }
                // println!("{:#?}", block);
                output.push("</div>\n".to_string());
            }
            _ => (), //println!("{:#?}", input),
        }
    }
    output.join("")
}
