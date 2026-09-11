<?php
declare(strict_types=1);

require_once __DIR__ . '/lib/phpmailer/Exception.php';
require_once __DIR__ . '/lib/phpmailer/PHPMailer.php';
require_once __DIR__ . '/lib/phpmailer/SMTP.php';

const RECIPIENT = 'ted@tedjohnsonworks.com';
const SUCCESS_URL = '/business.html?submitted=success#start-checkup';
const ERROR_URL = '/business.html?submitted=error#start-checkup';

function redirect_to(string $path): never
{
    header('Location: ' . $path, true, 303);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    http_response_code(405);
    exit('Method Not Allowed');
}

if (!empty($_POST['company_fax'] ?? '')) {
    redirect_to(SUCCESS_URL);
}

$startedAt = filter_input(INPUT_POST, 'form_started_at', FILTER_VALIDATE_INT);
$nowMs = (int) round(microtime(true) * 1000);
if (!$startedAt || $startedAt > $nowMs || ($nowMs - $startedAt) < 2000) {
    redirect_to(ERROR_URL);
}

$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
if (!$email || preg_match('/[\r\n]/', $email)) {
    redirect_to(ERROR_URL);
}

function clean_field(string $name, int $maxLength = 2000): string
{
    $value = trim((string) ($_POST[$name] ?? ''));
    $value = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/u', '', $value) ?? '';
    return mb_substr($value, 0, $maxLength);
}

$fields = [
    'Business Name' => clean_field('business_name', 200),
    'Your Name' => clean_field('your_name', 200),
    'What is harder than it should be?' => clean_field('challenge', 4000),
    'Email' => $email,
    'Phone' => clean_field('phone', 100),
    'Best way to reach you' => clean_field('best_contact', 100),
    'Website' => clean_field('website', 500),
    'City/State' => clean_field('city_state', 200),
];

$messageLines = ['A new Small Business Technology Checkup intake was submitted.', ''];
foreach ($fields as $label => $value) {
    $messageLines[] = $label . ':';
    $messageLines[] = $value !== '' ? $value : '(not provided)';
    $messageLines[] = '';
}

$configPath = dirname(__DIR__) . '/.tjw-private/mail-config.php';
if (!is_file($configPath)) {
    redirect_to(ERROR_URL);
}

$mailConfig = require $configPath;
$smtpPassword = is_array($mailConfig) ? (string) ($mailConfig['password'] ?? '') : '';
if ($smtpPassword === '' || $smtpPassword === 'PASTE_MAILBOX_PASSWORD_HERE') {
    redirect_to(ERROR_URL);
}

try {
    $mailer = new PHPMailer\PHPMailer\PHPMailer(true);
    $mailer->isSMTP();
    $mailer->Host = 'smtp.hostinger.com';
    $mailer->SMTPAuth = true;
    $mailer->Username = 'ted@tedjohnsonworks.com';
    $mailer->Password = $smtpPassword;
    $mailer->SMTPSecure = PHPMailer\PHPMailer\PHPMailer::ENCRYPTION_SMTPS;
    $mailer->Port = 465;
    $mailer->CharSet = 'UTF-8';
    $mailer->Timeout = 15;
    $mailer->setFrom('ted@tedjohnsonworks.com', 'Ted Johnson Works');
    $mailer->addAddress(RECIPIENT);
    $mailer->addReplyTo($email);
    $mailer->Subject = 'New TJW Technology Checkup Intake';
    $mailer->Body = implode("\n", $messageLines);
    $mailer->send();
    redirect_to(SUCCESS_URL);
} catch (Throwable $error) {
    error_log('TJW checkup form SMTP failure: ' . $error->getMessage());
    redirect_to(ERROR_URL);
}
